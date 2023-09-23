from django.urls import path

from robots import views
from robots.apps import RobotsConfig

app_name = RobotsConfig.name

urlpatterns = [
    path('create/', views.RobotCreateApiView.as_view(), name='create'),
]
