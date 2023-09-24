from django import views
from django.http import HttpResponse
from rest_framework import generics

from robots import models, serializers, services


class RobotCreateApiView(generics.CreateAPIView):
    queryset = models.Robot.objects.all()
    serializer_class = serializers.RobotSerializer


class DownloadSummaryView(views.View):
    def get(self, request):
        robot_summary = services.create_summary()
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'
        robot_summary.save(response)
        return response
