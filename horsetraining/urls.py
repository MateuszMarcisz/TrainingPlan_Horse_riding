from django.contrib import admin
from django.urls import path

from horsetraining.views import HomeView, TestView

urlpatterns = [
    path('testy', TestView.as_view(), name='test'),
]
