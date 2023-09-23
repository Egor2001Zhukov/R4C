import datetime

import openpyxl
from django import views
from django.http import HttpResponse
from rest_framework import generics

from robots import models, serializers


class RobotCreateApiView(generics.CreateAPIView):
    queryset = models.Robot.objects.all()
    serializer_class = serializers.RobotCreateSerializer


class DownloadSummaryView(views.View):
    def get(self, request):
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)
        data_for_last_week = models.Robot.objects.filter(created__range=(start_date, end_date))
        all_models = data_for_last_week.values('model').distinct()
        workbook = openpyxl.Workbook()
        for model in all_models:
            model_name = model.get('model')
            sheet = workbook.create_sheet(model_name)
            sheet.append(["Модель", "Версия", "Количество за неделю"])
            all_versions = data_for_last_week.filter(model=model_name).values('version').distinct()
            for version in all_versions:
                version_name = version.get('version')
                all_count = data_for_last_week.filter(model=model_name, version=version_name).count()
                print(model_name, version_name, all_count)
                sheet.append([model_name, version_name, all_count])
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'
        workbook.save(response)
        return response
