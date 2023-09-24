import datetime

import openpyxl

from robots import models


def create_summary():
    """Создаем и возвращаем сводку за последнюю неделю"""
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
            sheet.append([model_name, version_name, all_count])
    return workbook
