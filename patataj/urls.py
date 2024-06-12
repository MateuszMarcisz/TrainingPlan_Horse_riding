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
    path('plan_list/', views.PlanListView.as_view(), name='plan_list'),
    path('plan_detail/<int:pk>/', views.PlanDetailView.as_view(), name='plan_detail'),
    path('plan_add/', views.AddPlanView.as_view(), name='plan_add'),
    path('plan_delete/<int:pk>/', views.DeletePlanView.as_view(), name='plan_delete'),
    path('plan_edit/<int:pk>/', views.EditPlanView.as_view(), name='plan_edit'),
    path('horse_list/', views.HorseListView.as_view(), name='horse_list'),
    path('horse_detail/<int:pk>/', views.HorseDetailView.as_view(), name='horse_detail'),
    path('horse_add/', views.AddHorseView.as_view(), name='horse_add'),
    path('horse_delete/<int:pk>/', views.DeleteHorseView.as_view(), name='horse_delete'),
    path('horse_edit/<int:pk>/', views.EditHorseView.as_view(), name='horse_edit'),
    path('trainer_list/', views.TrainerListView.as_view(), name='trainer_list'),
    path('trainer_detail/<int:pk>/', views.TrainerDetailView.as_view(), name='trainer_detail'),
    path('trainer_add/', views.AddTrainerView.as_view(), name='trainer_add'),
    path('trainer_delete/<int:pk>/', views.DeleteTrainerView.as_view(), name='trainer_delete'),
]
