from django.contrib import admin
from django.urls import path
from patataj import views
from patataj.views import HomeView

urlpatterns = [
    path('testy/', views.TestView.as_view(), name='test'),
    path('training_list/', views.TrainingListView.as_view(), name='training_list'),
    path('training_detail/<int:pk>/', views.TrainingDetailView.as_view(), name='training_detail'),
    path('training_add', views.AddTrainingView.as_view(), name='training_add'),
    path('training_delete/<int:pk>/', views.DeleteTrainingView.as_view(), name='training_delete'),
    path('training_edit/<int:pk>/', views.EditTrainingView.as_view(), name='training_edit'),
]
