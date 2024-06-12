from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from patataj import models
from patataj.models import Training, TrainingType, Plan, Horse, Trainer


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')


class TestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'patataj/test.html')


class TrainingListView(View):
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
        paginator = Paginator(trainings, 5)  # we put 5 trainings per page
        page_number = request.GET.get('page', 1)  # in case there is no page select 1

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


class TrainingDetailView(View):
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
        return render(request, 'patataj/DeleteConfirmation.html', {'training': training})

    def post(self, request, pk):
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


class PlanListView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.GET.get('name')
        plans = models.Plan.objects.filter(user=request.user)
        if name:
            plans = plans.filter(name__icontains=name)
        # see training list view for some explanation of pagination
        paginator = Paginator(plans, 5)
        page_number = request.GET.get('page', 1)
        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)
        return render(request, 'patataj/PlanList.html', {'page_object': page_object})


class PlanDetailView(UserPassesTestMixin, View):
    def test_func(self):
        plan = models.Plan.objects.get(pk=self.kwargs['pk'])
        return self.request.user == plan.user

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        return render(request, 'patataj/PlanDetail.html', {'plan': plan})


class AddPlanView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'patataj/AddPlan.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        errors = {}
        if not name:
            errors['name'] = 'Nazwa wymagana!'
        if not description:
            errors['description'] = 'Opis wymagany!'
        if errors:
            return render(request, 'patataj/AddPlan.html', {
                'errors': errors,
                'name': name,
                'description': description,
            })

        try:
            plan = models.Plan.objects.create(
                name=name,
                description=description,
                user_id=request.user.id,
            )
            return redirect('plan_detail', pk=plan.pk)

        except Exception as e:
            return render(request, 'patataj/AddPlan.html', {
                'errors': e,
            })


class DeletePlanView(UserPassesTestMixin, View):
    def test_func(self):
        plan = models.Plan.objects.get(pk=self.kwargs['pk'])
        return self.request.user == plan.user

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        return render(request, 'patataj/DeletePlanConfirmation.html', {'plan': plan})

    def post(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        plan.delete()
        return redirect('plan_list')


class EditPlanView(UserPassesTestMixin, View):
    def test_func(self):
        plan = models.Plan.objects.get(pk=self.kwargs['pk'])
        return self.request.user == plan.user

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        return render(request, 'patataj/PlanEdit.html', {'plan': plan})

    def post(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        name = request.POST.get('name')
        description = request.POST.get('description')
        errors = {}
        if not name:
            errors['name'] = 'Nazwa wymagana!'
        if not description:
            errors['description'] = 'Opis wymagany!'
        if errors:
            return render(request, 'patataj/PlanEdit.html', {
                'errors': errors,
                'name': name,
                'description': description,
                'plan': plan
            })
        try:
            plan.name = name
            plan.description = description
            plan.save()
            return redirect('plan_detail', pk=plan.pk)
        except Exception as e:
            return render(request, 'patataj/PlanEdit.html', {'errors': e})


class HorseListView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.GET.get('name')
        horses = models.Horse.objects.filter(owner=request.user)
        if name:
            horses = horses.filter(name__icontains=name)
        # see training list view for some explanation of pagination
        paginator = Paginator(horses, 5)
        page_number = request.GET.get('page', 1)
        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)
        return render(request, 'patataj/HorseList.html', {'page_object': page_object})


class HorseDetailView(UserPassesTestMixin, View):
    def test_func(self):
        horse = models.Horse.objects.get(pk=self.kwargs['pk'])
        return self.request.user == horse.owner

    def get(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        return render(request, 'patataj/HorseDetail.html', {'horse': horse})


class AddHorseView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'patataj/AddHorse.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        errors = {}
        if not name:
            errors['name'] = 'Imię konia jest wymagane!'
        if not description:
            errors['description'] = 'Opis konia jest wymagany!'
        if errors:
            return render(request, 'patataj/AddHorse.html', {
                'errors': errors,
                'name': name,
                'description': description,
            })

        try:
            plan = models.Horse.objects.create(
                name=name,
                description=description,
                owner_id=request.user.id,
            )
            return redirect('horse_detail', pk=plan.pk)

        except Exception as e:
            return render(request, 'patataj/AddHorse.html', {
                'errors': e,
            })


class DeleteHorseView(UserPassesTestMixin, View):
    def test_func(self):
        horse = models.Horse.objects.get(pk=self.kwargs['pk'])
        return self.request.user == horse.owner

    def get(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        return render(request, 'patataj/DeleteHorseConfirmation.html', {'horse': horse})

    def post(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        horse.delete()
        return redirect('horse_list')


class EditHorseView(UserPassesTestMixin, View):
    def test_func(self):
        horse = Horse.objects.get(pk=self.kwargs['pk'])
        return self.request.user == horse.owner

    def get(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        return render(request, 'patataj/HorseEdit.html', {'horse': horse})

    def post(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        name = request.POST.get('name')
        description = request.POST.get('description')
        errors = {}
        if not name:
            errors['name'] = 'Imię konia jest wymagane!'
        if not description:
            errors['description'] = 'Opis konia jest wymagany!'
        if errors:
            return render(request, 'patataj/HorseEdit.html', {
                'errors': errors,
                'name': name,
                'description': description,
                'horse': horse
            })
        try:
            horse.name = name
            horse.description = description
            horse.save()
            return redirect('horse_detail', pk=horse.pk)
        except Exception as e:
            return render(request, 'patataj/HorseEdit.html', {'errors': e})


class TrainerListView(View):
    def get(self, request):
        name = request.GET.get('name', '')
        training_type = request.GET.get('training_type', '')
        trainers = Trainer.objects.all()
        training_type_choices = TrainingType.choices

        # Filtering
        if name:
            trainers = trainers.filter(name__icontains=name)
        if training_type:
            trainers = trainers.filter(training_type=training_type)

        # Pagination
        # see TrainingListView for more details
        paginator = Paginator(trainers, 5)
        page_number = request.GET.get('page', 1)
        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        return render(request, 'patataj/TrainerList.html', {
            'page_object': page_object,
            'training_type_choices': training_type_choices
        })
