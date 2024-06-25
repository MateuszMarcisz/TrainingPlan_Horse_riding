from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from trainingplans import models
from trainingplans.forms import TrainingPlanForm, TrainingToAnyPlanForm, TrainerForm
from trainingplans.models import Training, TrainingType, Plan, Horse, Trainer, TrainingPlan, TrainingPlanDay


def pagination(request, queryset, items_per_page=5):
    paginator = Paginator(queryset, items_per_page)  # we define what should be paginated and how many elements per page
    page_number = request.GET.get('page', 1)  # in case there is no page select 1
    try:
        page_object = paginator.page(page_number)
    except PageNotAnInteger:  # handling annoying user manually changing stuff
        page_object = paginator.page(1)
    except EmptyPage:  # again, annoying user, when out of range page
        page_object = paginator.page(paginator.num_pages)
    return page_object


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'trainingplans/homepage.html')


class TestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'trainingplans/test.html')


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
        page_object = pagination(request, trainings)

        return render(request, 'trainingplans/TrainingList.html', {
            'page_object': page_object,  # Pass paginated queryset to template
            'training_type_choices': training_type_choices
        })


class TrainingDetailView(View):
    def get(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        return render(request, 'trainingplans/TrainingDetail.html', {'training': training})


class AddTrainingView(LoginRequiredMixin, View):
    def get(self, request):
        training_type_choices = TrainingType.choices
        return render(request, 'trainingplans/AddTraining.html', {'training_type_choices': training_type_choices})

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
            return render(request, 'trainingplans/AddTraining.html', {
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
            return render(request, 'trainingplans/AddTraining.html', {
                'errors': e,
                'training_type_choices': training_type_choices
            })


class DeleteTrainingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        return render(request, 'trainingplans/DeleteConfirmation.html', {'training': training})

    def post(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        training.delete()
        return redirect('training_list')


class EditTrainingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        training = get_object_or_404(Training, pk=pk)
        training_type_choices = TrainingType.choices
        return render(request, 'trainingplans/TrainingEdit.html', {
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
            return render(request, 'trainingplans/TrainingEdit.html', {
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
            return render(request, 'trainingplans/TrainingEdit.html', {
                'errors': e,
                'training_type_choices': training_type_choices
            })


class PlanListView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.GET.get('name')
        plans = models.Plan.objects.filter(user=request.user)
        if name:
            plans = plans.filter(name__icontains=name)
        # see pagination function for some explanation of pagination
        page_object = pagination(request, plans)
        return render(request, 'trainingplans/PlanList.html', {'page_object': page_object})


class PlanDetailView(UserPassesTestMixin, View):
    def test_func(self):
        plan = models.Plan.objects.get(pk=self.kwargs['pk'])
        return self.request.user == plan.user

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        days_plan = TrainingPlan.objects.filter(plan=plan).order_by('day', 'time')

        # We group trainings by the days
        trainings_by_day = {day.label: [] for day in TrainingPlanDay}
        for training_plan in days_plan:
            day = training_plan.get_day_display()
            trainings_by_day[day].append(training_plan)

        # We show only days that have something happening in them (so there is a training in those days)
        trainings_by_day = {day: trainings for day, trainings in trainings_by_day.items() if trainings}

        return render(request, 'trainingplans/PlanDetail.html', {
            'plan': plan,
            'trainings_by_day': trainings_by_day,
        })


class AddPlanView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'trainingplans/AddPlan.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        errors = {}
        if not name:
            errors['name'] = 'Nazwa wymagana!'
        if not description:
            errors['description'] = 'Opis wymagany!'
        if errors:
            return render(request, 'trainingplans/AddPlan.html', {
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
            return render(request, 'trainingplans/AddPlan.html', {
                'errors': e,
            })


class DeletePlanView(UserPassesTestMixin, View):
    def test_func(self):
        plan = models.Plan.objects.get(pk=self.kwargs['pk'])
        return self.request.user == plan.user

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        return render(request, 'trainingplans/DeletePlanConfirmation.html', {'plan': plan})

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
        return render(request, 'trainingplans/PlanEdit.html', {'plan': plan})

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
            return render(request, 'trainingplans/PlanEdit.html', {
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
            return render(request, 'trainingplans/PlanEdit.html', {'errors': e})


class HorseListView(LoginRequiredMixin, View):
    def get(self, request):
        name = request.GET.get('name')
        horses = models.Horse.objects.filter(owner=request.user)
        if name:
            horses = horses.filter(name__icontains=name)
        # see pagination function for details
        page_object = pagination(request, horses)
        return render(request, 'trainingplans/HorseList.html', {'page_object': page_object})


class HorseDetailView(UserPassesTestMixin, View):
    def test_func(self):
        horse = models.Horse.objects.get(pk=self.kwargs['pk'])
        return self.request.user == horse.owner

    def get(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        return render(request, 'trainingplans/HorseDetail.html', {'horse': horse})


class AddHorseView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'trainingplans/AddHorse.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        errors = {}
        if not name:
            errors['name'] = 'Imię konia jest wymagane!'
        if not description:
            errors['description'] = 'Opis konia jest wymagany!'
        if errors:
            return render(request, 'trainingplans/AddHorse.html', {
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
            return render(request, 'trainingplans/AddHorse.html', {
                'errors': e,
            })


class DeleteHorseView(UserPassesTestMixin, View):
    def test_func(self):
        horse = models.Horse.objects.get(pk=self.kwargs['pk'])
        return self.request.user == horse.owner

    def get(self, request, pk):
        horse = get_object_or_404(Horse, pk=pk)
        return render(request, 'trainingplans/DeleteHorseConfirmation.html', {'horse': horse})

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
        return render(request, 'trainingplans/HorseEdit.html', {'horse': horse})

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
            return render(request, 'trainingplans/HorseEdit.html', {
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
            return render(request, 'trainingplans/HorseEdit.html', {'errors': e})


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
        page_object = pagination(request, trainers)

        return render(request, 'trainingplans/TrainerList.html', {
            'page_object': page_object,
            'training_type_choices': training_type_choices
        })


class TrainerDetailView(View):
    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        return render(request, 'trainingplans/TrainerDetail.html', {'trainer': trainer})


class AddTrainerView(LoginRequiredMixin, View):

    def get(self, request):
        form = TrainerForm()
        return render(request, 'trainingplans/AddTrainer.html', {'form': form})

    def post(self, request):
        form = TrainerForm(request.POST)
        if form.is_valid():
            trainer = form.save()
            return redirect('trainer_detail', pk=trainer.pk)
        else:
            return render(request, 'trainingplans/AddTrainer.html', {'form': form})

    # def get(self, request):
    #     training_type_choices = TrainingType.choices
    #     return render(request, 'patataj/AddTrainer.html', {'training_type_choices': training_type_choices})
    #
    # def post(self, request):
    #     name = request.POST.get('name')
    #     training_type = request.POST.get('training_type')
    #     description = request.POST.get('description')
    #     training_type_choices = TrainingType.choices
    #     errors = {}
    #     if not name:
    #         errors['name'] = 'Imię/Nazwisko trenera jest wymagane!'
    #     if not training_type:
    #         errors['training_type'] = 'Typ treningu jest wymagany!'
    #     if not description:
    #         errors['description'] = 'Opis trenera jest wymagany!'
    #     if errors:
    #         return render(request, 'patataj/AddTrainer.html', {
    #             'errors': errors,
    #             'name': name,
    #             'training_type': training_type,
    #             'description': description,
    #             'training_type_choices': training_type_choices
    #         })
    #
    #     try:
    #         trainer = Trainer.objects.create(
    #             name=name,
    #             training_type=training_type,
    #             description=description
    #         )
    #         return redirect('trainer_detail', pk=trainer.pk)
    #
    #     except Exception as e:
    #         return render(request, 'patataj/AddTrainer.html', {
    #             'errors': e,
    #             'training_type_choices': training_type_choices
    #         })


class DeleteTrainerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        return render(request, 'trainingplans/DeleteTrainerConfirmation.html', {'trainer': trainer})

    def post(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        trainer.delete()
        return redirect('trainer_list')


class EditTrainerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        training_type_choices = TrainingType.choices
        return render(request, 'trainingplans/TrainerEdit.html', {
            'trainer': trainer,
            'training_type_choices': training_type_choices
        })

    def post(self, request, pk):
        name = request.POST.get('name')
        training_type = request.POST.get('training_type')
        description = request.POST.get('description')
        training_type_choices = TrainingType.choices
        trainer = get_object_or_404(Trainer, pk=pk)
        errors = {}
        if not name:
            errors['name'] = 'Imię/Nazwisko trenera jest wymagane!'
        if not training_type:
            errors['training_type'] = 'Typ treningu jest wymagany!'
        if not description:
            errors['description'] = 'Opis trenera jest wymagany!'
        if errors:
            return render(request, 'trainingplans/TrainerEdit.html', {
                'errors': errors,
                'name': name,
                'training_type': training_type,
                'description': description,
                'training_type_choices': training_type_choices,
                'trainer': trainer
            })

        try:
            trainer.name = name
            trainer.training_type = training_type
            trainer.description = description
            trainer.save()
            return redirect('trainer_detail', pk=trainer.pk)

        except Exception as e:
            return render(request, 'trainingplans/TrainerEdit.html', {
                'errors': e,
                'training_type_choices': training_type_choices
            })


class TrainingToPlanAdd(UserPassesTestMixin, View):
    def test_func(self):
        plan = Plan.objects.get(pk=self.kwargs['pk'])
        return self.request.user == plan.user

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        form = TrainingPlanForm(user=request.user)
        return render(request, 'trainingplans/AddTrainingToPlan.html', {
            'plan': plan,
            'form': form
        })

    def post(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        form = TrainingPlanForm(request.POST, user=request.user)
        if form.is_valid():
            training_plan = form.save(commit=False)
            training_plan.plan = plan
            training_plan.save()
            return redirect('plan_detail', pk=plan.pk)
        return render(request, 'trainingplans/AddTrainingToPlan.html', {
            'plan': plan,
            'form': form
        })


class TrainingToAnyPlanAdd(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request):
        form = TrainingToAnyPlanForm(user=request.user)
        return render(request, 'trainingplans/AddTrainingToAnyPlan.html', {'form': form})

    def post(self, request):
        form = TrainingToAnyPlanForm(request.POST, user=request.user)
        if form.is_valid():
            # We do not commit yet, we need to get missing data
            training_plan = form.save(commit=False)

            # Fetch the selected plan from the form data
            plan_id = request.POST.get('plan')
            plan = Plan.objects.get(pk=plan_id)

            # Assign the plan to the training plan instance
            training_plan.plan = plan
            training_plan.save()

            # Redirect to the plan_detail
            return redirect('plan_detail', pk=plan.pk)

        return render(request, 'trainingplans/AddTrainingToAnyPlan.html', {'form': form})


class DeleteTrainingFromPlanView(UserPassesTestMixin, View):
    def test_func(self):
        training_plan = get_object_or_404(TrainingPlan, pk=self.kwargs['pk'])
        return training_plan.plan.user == self.request.user

    def get(self, request, pk):
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        return render(request, 'trainingplans/DeleteTrainingFromPlanConfirmation.html', {'training_plan': training_plan})

    def post(self, request, pk):
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        training_plan.delete()
        return redirect('plan_detail', pk=training_plan.plan.pk)
