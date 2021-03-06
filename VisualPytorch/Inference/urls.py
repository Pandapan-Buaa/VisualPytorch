from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resnet18/$', views.Resnet18.as_view()),
    url(r'^dcgan/$', views.Dcgan.as_view()),
    url(r'^frcnn/$', views.Frcnn.as_view()),
    url(r'^unet/$', views.Unet.as_view()),
    url(r'^resnet101/$', views.Resnet101.as_view()),
]
