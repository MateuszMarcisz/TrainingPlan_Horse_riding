from django.urls import path
from .views import CalendarView, AddEventView

urlpatterns = [
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('add_event/', AddEventView.as_view(), name='add_event'),
    ]