from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Event
from .forms import EventForm


class CalendarView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'kalendarz/calendar.html', {'events': events})


class AddEventView(LoginRequiredMixin, View):
    def get(self, request):
        form = EventForm()
        return render(request, 'kalendarz/add_event.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendar')
        return render(request, 'kalendarz/add_event.html', {'form': form})
