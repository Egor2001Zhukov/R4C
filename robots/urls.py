from django.urls import path

from robots import views
from robots.apps import RobotsConfig

app_name = RobotsConfig.name

urlpatterns = [
    path('create/', views.RobotCreateApiView.as_view(), name='create'),
    path('download_summary/', views.DownloadSummaryView.as_view(), name='download_summary'),

]
