from django.contrib import admin
from django.urls import path
from patataj import views
from patataj.views import HomeView

urlpatterns = [
    path('testy/', views.TestView.as_view(), name='test'),
    path('training_list/', views.TrainingListView.as_view(), name='training_list'),
    path('training_detail/<int:pk>/', views.TrainingDetailView.as_view(), name='training_detail'),
]
