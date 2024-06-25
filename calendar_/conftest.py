import pytest
from django.contrib.auth.models import User

from calendar_.models import Event


@pytest.fixture
def user():
    return User.objects.create(username='test')


@pytest.fixture
def events(user):
    lst = []
    for i in range(10):
        lst.append(Event.objects.create(
            user=user,
            title=i,
            description=i,
            start_time='2024-06-16 11:15:00',
            end_time='2024-06-16 12:15:00'
        ))
    return lst


@pytest.fixture
def event(user):
    return Event.objects.create(
        user=user,
        title='Event Title',
        description='Event Description',
        start_time='2024-06-16 11:15:00',
        end_time='2024-06-16 12:15:00'
    )
