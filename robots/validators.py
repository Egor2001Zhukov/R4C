from rest_framework import serializers


class ModelVersionValidator:
    def __call__(self, value: str):
        if len(value) != 2:
            raise serializers.ValidationError("Поле должно состоять из 2 символов")
