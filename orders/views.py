from django.views import generic

from customers.models import Customer
from orders import forms
from orders import models
from orders import services


class OrderCreateView(generic.CreateView):
    model = models.Order
    form_class = forms.OrderForm

    def form_valid(self, form):
        """Получаем из формы email клиента для создания заказа, если он еще не покупал робота, сохраняем его в базе данных.
        Сохраняем заказ от этого клиента и идем проверять наличие робота.
        Также если клиент неправильно указал формат серии робота, добавляется ошибка и форма перезагружается"""
        if form.is_valid():
            if services.validate_robot_serial(form.cleaned_data.get('robot_serial')):
                email = form.cleaned_data.pop('email')
                customer = Customer.objects.get_or_create(email=email)[0]
                new_order = form.save(commit=False)
                new_order.customer = customer
                new_order.save()
                self.success_url = services.order_processing(new_order)
                return super().form_valid(form)
            else:
                form.add_error('robot_serial', 'Формат должен быть "**-**"')
                return self.form_invalid(form)
