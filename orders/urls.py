from django.urls import path
from django.views.generic import TemplateView

from orders import views
from orders.apps import OrdersConfig

app_name = OrdersConfig.name

urlpatterns = [

    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('success_order/', TemplateView.as_view(template_name='orders/success_order.html'), name='success_order'),
    path('wait_arrival/', TemplateView.as_view(template_name='orders/wait_arrival.html'), name='wait_arrival'),

]
