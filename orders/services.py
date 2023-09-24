import re

from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse

from R4C import settings
from orders import models
from robots.models import Robot
from robots.serializers import robot_created_signal


def validate_robot_serial(value):
    """Валидация формата серии робота при его заказе"""
    pattern = r'^[A-Z0-9]{1,2}-[A-Z0-9]{1,2}$'
    if not re.match(pattern, value):
        return False
    return True


def order_processing(order):
    """Проверка наличия робота """
    robot_in_stock = Robot.objects.filter(serial=order.robot_serial, in_stock=True).first()
    if robot_in_stock:
        robot_in_stock.in_stock = False
        robot_in_stock.save()
        order.is_completed = True
        order.save()
        return reverse('orders:success_order')
    return reverse('orders:wait_arrival')


@receiver(robot_created_signal, sender=Robot)
def report_receipt(instance, **kwargs):
    """Принимаем сигнал при создании робота и проверяем есть ли заказ на него. Если их несколько заказ оформиться на того кто первее заказал"""
    order = models.Order.objects.filter(is_completed=False, robot_serial=instance.serial).order_by('created').first()
    if order:
        order.is_completed = True
        order.save()
        instance.in_stock = False
        instance.save()
        subject = 'Заказ робота'
        message = f'Добрый день! Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. ' \
                  f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        send_mail(subject=subject, message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[order.customer.email])
