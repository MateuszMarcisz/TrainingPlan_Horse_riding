from django.contrib import admin
from django.urls import path

from patataj.views import HomeView, TestView, TrainingListView

urlpatterns = [
    path('testy', TestView.as_view(), name='test'),
    path('training_list', TrainingListView.as_view(), name='training_list'),
]
