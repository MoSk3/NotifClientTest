from django.urls import path

from . import views, consumers

urlpatterns = [
    path('', views.index),
]

ws_urlpatterns = [
    path('iotgateway', consumers.IoTDeviceConsumer.as_asgi()),
    path('usergateway', consumers.IoTUserConsumer.as_asgi()),
]