from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TrainingType(models.TextChoices):
    SKOKOWY = 'SK', 'Skokowy'
    UJEŻDŻENIOWY = 'UJ', 'Ujeżdżeniowy'
    LONŻA = 'LO', 'Lonża'
    PRACA_Z_ZIEMI = 'PZ', 'Praca z ziemi'
    TEREN = 'TE', 'Teren'
    CROSS = 'CR', 'Cross'


class Training(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=2,
        choices=TrainingType.choices,
    )
    description = models.TextField()
    length = models.IntegerField()

    def __str__(self):
        return f"{self.name} typu {self.get_type_display()} o długości {self.length} min"


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    trainings = models.ManyToManyField(Training, through='TrainingPlan')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TrainingPlanDay(models.TextChoices):
    PONIEDZIAŁEK = 'PN', 'Poniedziałek'
    WTOREK = 'WT', 'Wtorek'
    ŚRODA = 'SR', 'Środa'
    CZWARTEK = 'CZ', 'Czwartek'
    PIĄTEK = 'PT', 'Piątek'
    SOBOTA = 'SB', 'Sobota'
    NIEDZIELA = 'ND', 'Niedziela'


class Horse(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    training_type = models.CharField(
        max_length=2,
        choices=TrainingType.choices
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} trening: {self.get_training_type_display()}"


class TrainingPlan(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day = models.CharField(
        max_length=2,
        choices=TrainingPlanDay.choices,
        default=TrainingPlanDay.PONIEDZIAŁEK
    )
    time = models.TimeField()
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plan.name} - {self.training.name} - {self.training.type} w {self.get_day_display()} o {self.time}"
