from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from patataj import models
from patataj.models import Training, TrainingType


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')


class TestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'patataj/test.html')


class TrainingListView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.GET.get('name', '')
        training_type = request.GET.get('training_type', '')
        min_length = request.GET.get('min_length', '0')
        trainings = Training.objects.all()
        training_type_choices = TrainingType.choices

        # Filtering
        if name:
            trainings = trainings.filter(name__icontains=name)
        if training_type:
            trainings = trainings.filter(type__icontains=training_type)
        try:
            min_length = int(min_length)
            if min_length >= 0:
                trainings = trainings.filter(length__gte=min_length)
            elif min_length < 0:
                raise ValueError("Długość treningu nie może być ujemna.")
        except ValueError as e:
            messages.error(request, str(e))

        # Pagination
        paginator = Paginator(trainings, 10)
        page_number = request.GET.get('page')

        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:  # handling annoying user manually changing stuff
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)  # again, annoying user, when out of range page

        return render(request, 'patataj/TrainingList.html', {
            'page_object': page_object,  # Pass paginated queryset to template
            'training_type_choices': training_type_choices
        })


class TrainingDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        training = models.Training.objects.get(pk=pk)
        return render(request, 'patataj/TrainingDetail.html', {'training': training})
