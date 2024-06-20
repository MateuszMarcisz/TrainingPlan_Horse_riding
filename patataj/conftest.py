import pytest
from django.contrib.auth.models import User

from patataj.models import Training, Plan, Horse, Trainer, TrainingPlan


@pytest.fixture
def trainings():
    lst = []
    for i in range(15):
        lst.append(Training.objects.create(
            name=f"Training {i}",
            type="SK",
            description="Test description",
            length=30))
    return lst


@pytest.fixture
def training():
    return Training.objects.create(name="name", type="SK", description="description", length=30)


@pytest.fixture
def user():
    return User.objects.create(username='test')


@pytest.fixture
def user2():
    return User.objects.create(username='test2')


@pytest.fixture
def plans(user):
    lst = []
    for i in range(15):
        lst.append(Plan.objects.create(name=i, description="description", user_id=user.id))
    return lst


@pytest.fixture
def plan(user):
    return Plan.objects.create(name="name", description="description", user_id=user.id)


@pytest.fixture
def plan2(user2):
    return Plan.objects.create(name="name2", description="description2", user_id=user2.id)


@pytest.fixture
def horses(user):
    lst = []
    for i in range(15):
        lst.append(Horse.objects.create(name=i, description="description", owner_id=user.id))
    return lst


@pytest.fixture
def horse(user):
    return Horse.objects.create(name="name", description="description", owner_id=user.id)


@pytest.fixture
def trainers():
    lst = []
    for i in range(15):
        lst.append(Trainer.objects.create(name=i, training_type='SK', description='description'))
    return lst


@pytest.fixture
def trainer():
    return Trainer.objects.create(name='name', training_type='SK', description='description')


@pytest.fixture
def training_plans(trainer, training, horse, plan):
    lst = []
    for i in range(15):
        lst.append(TrainingPlan.objects.create(
            training_id=training.id,
            horse_id=horse.id,
            plan_id=plan.id,
            day='WT',
            trainer_id=trainer.id,
            time='06:45:00'
        ))
    return lst
