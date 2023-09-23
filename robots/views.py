from rest_framework import generics

from robots import models, serializers


class RobotCreateApiView(generics.CreateAPIView):
    queryset = models.Robot.objects.all()
    serializer_class = serializers.RobotCreateSerializer
