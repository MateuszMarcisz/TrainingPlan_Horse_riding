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
    length = models.DurationField()

    def __str__(self):
        return f"{self.name} typu {self.type} o długości {self.length}"


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    trainings = models.ManyToManyField(Training, through='TrainingPlan')

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
    description = models.TextField()
    users = models.ManyToManyField(User, through='UserTrainer')

    def __str__(self):
        return f"{self.name} trening: {self.training_type}"


class UserTrainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)


class TrainingPlan(models.Model):
    name = models.CharField(max_length=100)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day = models.CharField(
        max_length=2,
        choices=TrainingPlanDay.choices,
        default=TrainingPlanDay.PONIEDZIAŁEK
    )
    time = models.TimeField()
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.plan.name} - {self.training.name} w {self.get_day_display()} o {self.time}"
