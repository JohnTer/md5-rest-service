from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'submit', views.TaskCreateEnv.as_view(), name='submit'),
    path(r'check', views.TaskCheckView.as_view(), name='check'),
]