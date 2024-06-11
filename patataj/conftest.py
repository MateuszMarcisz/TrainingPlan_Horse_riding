import pytest
from django.contrib.auth.models import User

from patataj.models import Training, Plan


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
def plans(user):
    lst = []
    for i in range(15):
        lst.append(Plan.objects.create(name=i, description="description", user_id=user.id))
    return lst


@pytest.fixture
def plan(user):
    return Plan.objects.create(name="name", description="description", user_id=user.id)
