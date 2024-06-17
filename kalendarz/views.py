from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Event
from .forms import EventForm, EventEditForm
from django.middleware.csrf import get_token


class CalendarView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'kalendarz/calendar.html', {'events': events})


class AddEventView(LoginRequiredMixin, View):
    def get(self, request):
        initial_data = {}
        date = request.GET.get('date')
        if date:
            initial_data['start_time'] = f"{date}T18:00"
            initial_data['end_time'] = f"{date}T19:00"

        form = EventForm(initial=initial_data)
        return render(request, 'kalendarz/add_event.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendar')
        return render(request, 'kalendarz/add_event.html', {'form': form})


class EventDetailView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        return render(request, 'kalendarz/event_detail.html', {'event': event})


class EventEditView(UserPassesTestMixin, View):
    def test_func(self):
        pk = self.kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        return self.request.user == event.user

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = EventEditForm(instance=event)
        return render(request, 'kalendarz/edit_event.html', {'form': form, 'event': event})

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendar')
        return render(request, 'kalendarz/edit_event.html', {'form': form, 'event': event})


class EventDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        pk = self.kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        return self.request.user == event.user

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'kalendarz/event_delete_confirm.html', {'event': event})

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return redirect('calendar')
