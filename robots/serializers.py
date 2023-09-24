from django.dispatch import Signal
from rest_framework import serializers

from robots import models
from robots.validators import ModelVersionValidator

robot_created_signal = Signal()


class RobotSerializer(serializers.ModelSerializer):
    model = serializers.CharField(validators=[ModelVersionValidator()])
    version = serializers.CharField(validators=[ModelVersionValidator()])
    serial = serializers.SerializerMethodField()

    def get_serial(self, obj: models.Robot):
        return f'{obj.model}-{obj.version}'

    class Meta:
        model = models.Robot
        fields = '__all__'

    def create(self, validated_data):
        """При отправке post-запроса, мы берем валидные данные модели и версии,
        собираем из них серию и отправляем сигнал для поиска заказа на него"""
        model = validated_data.get('model')
        version = validated_data.get('version')
        created = validated_data.get('created')
        robot = models.Robot.objects.create(model=model, version=version, serial=f'{model}-{version}', created=created)
        robot_created_signal.send(sender=models.Robot, instance=robot)
        return robot
