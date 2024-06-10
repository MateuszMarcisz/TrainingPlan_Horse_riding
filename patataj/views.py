from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
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


class AddTrainingView(LoginRequiredMixin, View):
    def get(self, request):
        training_type_choices = TrainingType.choices
        return render(request, 'patataj/AddTraining.html', {'training_type_choices': training_type_choices})

    def post(self, request):
        name = request.POST.get('name')
        training_type = request.POST.get('training_type')
        length = request.POST.get('length')
        description = request.POST.get('description')
        training_type_choices = TrainingType.choices

        errors = {}
        if not name:
            errors['name'] = 'Nazwa wymagana!'
        if not training_type:
            errors['training_type'] = 'Typ wymagany!'
        if not length:
            errors['length'] = 'Długość wymagana!'
        if not description:
            errors['description'] = 'Opis wymagany!'
        if errors:
            return render(request, 'patataj/AddTraining.html', {
                'errors': errors,
                'name': name,
                'training_type': training_type,
                'length': length,
                'description': description,
                'training_type_choices': training_type_choices
            })

        try:
            training = models.Training.objects.create(
                name=name,
                type=training_type,
                length=length,
                description=description
            )
            return redirect('training_detail', pk=training.pk)

        except Exception as e:
            return render(request, 'patataj/AddTraining.html', {
                'errors': e,
                'training_type_choices': training_type_choices
            })


class DeleteTrainingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        training.delete()
        return redirect('training_list')


class EditTrainingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        training_type_choices = TrainingType.choices
        return render(request, 'patataj/TrainingEdit.html', {
            'training': training,
            'training_type_choices': training_type_choices
        })

    def post(self, request, pk):
        name = request.POST.get('name')
        training_type = request.POST.get('training_type')
        length = request.POST.get('length')
        description = request.POST.get('description')
        training_type_choices = TrainingType.choices
        training = models.Training.objects.get(pk=pk)

        errors = {}
        if not name:
            errors['name'] = 'Nazwa wymagana!'
        if not training_type:
            errors['training_type'] = 'Typ wymagany!'
        if not length:
            errors['length'] = 'Długość wymagana!'
        if not description:
            errors['description'] = 'Opis wymagany!'
        if errors:
            return render(request, 'patataj/TrainingEdit.html', {
                'errors': errors,
                'name': name,
                'training_type': training_type,
                'length': length,
                'description': description,
                'training_type_choices': training_type_choices,
                'training': training
            })

        try:
            training.name = name
            training.type = training_type
            training.length = length
            training.description = description
            training.save()
            return redirect('training_detail', pk=training.pk)

        except Exception as e:
            return render(request, 'patataj/TrainingEdit.html', {
                'errors': e,
                'training_type_choices': training_type_choices
            })
