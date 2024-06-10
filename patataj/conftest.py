import pytest

from patataj.models import Training


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
