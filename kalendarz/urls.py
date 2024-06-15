from django.urls import path
from .views import CalendarView, AddEventView, EventDetailView, EventEditView

urlpatterns = [
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('add_event/', AddEventView.as_view(), name='add_event'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event_edit/<int:pk>/', EventEditView.as_view(), name='event_edit'),
    ]
