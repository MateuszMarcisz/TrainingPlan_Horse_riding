from django import forms
from .models import TrainingPlan, Training, Horse, Trainer, Plan, TrainingType


# We can adjust what is display in the choices either by editing __str__ in models, but if we do not want to do that,
# we could do something like that:
# class TrainingChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.name
# and then below in the Training PlanForm change "forms.ModelChoiceField" into "TrainingChoiceField"


class TrainingPlanForm(forms.ModelForm):
    training = forms.ModelChoiceField(
        queryset=Training.objects.all(),
        empty_label="Wybierz trening",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    horse = forms.ModelChoiceField(
        queryset=Horse.objects.none(),  # Initialize with an empty queryset
        empty_label="Wybierz konia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        empty_label="Wybierz trenera (opcjonalne)",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TrainingPlan
        fields = ['training', 'day', 'time', 'horse', 'trainer']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):  # to jest po to, aby pokazać tylko konie danego usera
        user = kwargs.pop('user', None)
        super(TrainingPlanForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['horse'].queryset = Horse.objects.filter(owner=user)


class TrainingToAnyPlanForm(forms.ModelForm):
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.none(),  # Initialize with an empty queryset
        empty_label="Wybierz plan",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    training = forms.ModelChoiceField(
        queryset=Training.objects.all(),
        empty_label="Wybierz trening",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    horse = forms.ModelChoiceField(
        queryset=Horse.objects.none(),
        empty_label="Wybierz konia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        empty_label="Wybierz trenera (opcjonalne)",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TrainingPlan
        fields = ['plan', 'training', 'day', 'time', 'horse', 'trainer']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TrainingToAnyPlanForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['plan'].queryset = Plan.objects.filter(user=user)
            self.fields['horse'].queryset = Horse.objects.filter(owner=user)


class TrainerForm(forms.ModelForm):
    training_type = forms.ChoiceField(
        choices=[('', 'wybierz typ treningu')] + list(TrainingType.choices),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Trainer
        fields = ['name', 'training_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'name': {
                'required': 'Imię/Nazwisko trenera jest wymagane!'
            },
            'training_type': {
                'required': 'Typ treningu jest wymagany!'
            },
        }
