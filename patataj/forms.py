from django import forms
from .models import TrainingPlan, Training, Horse, Trainer


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
        empty_label="Wybierz trenera",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TrainingPlan
        fields = ['name', 'training', 'day', 'time', 'horse', 'trainer']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Podaj Nazwę'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):  # to jest po to, aby pokazać tylko konie danego usera
        user = kwargs.pop('user', None)
        super(TrainingPlanForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['horse'].queryset = Horse.objects.filter(owner=user)
