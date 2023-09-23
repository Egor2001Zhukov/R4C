from rest_framework import serializers

from robots import models
from robots.validators import ModelVersionValidator


class RobotCreateSerializer(serializers.ModelSerializer):
    model = serializers.CharField(validators=[ModelVersionValidator()])
    version = serializers.CharField(validators=[ModelVersionValidator()])
    serial = serializers.SerializerMethodField()

    def get_serial(self, obj: models.Robot):
        return f'{obj.model}-{obj.version}'

    class Meta:
        model = models.Robot
        fields = '__all__'
