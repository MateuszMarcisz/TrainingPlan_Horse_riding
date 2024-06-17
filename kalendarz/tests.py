import datetime

import pytest
from django.test import TestCase, Client
from django.urls import reverse

from kalendarz.models import Event


# Create your tests here.
@pytest.mark.django_db
def test_calendar_view_works():
    client = Client()
    url = reverse('calendar')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_calendar_view_events(events):
    client = Client()
    url = reverse('calendar')
    response = client.get(url)
    assert response.status_code == 200
    assert len(events) == len(response.context['events'])
    assert len(response.context['events']) == 10


@pytest.mark.django_db
def test_add_event_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_event')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_event_get_not_logged():
    client = Client()
    url = reverse('add_event')
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_add_event_post(user):
    client = Client()
    client.force_login(user)
    data = {
        'user': 'user',
        'title': 'Event Title',
        'description': 'Event Description',
        'start_time': '2024-06-16 11:15:00',
        'end_time': '2024-06-16 12:15:00'
    }
    url = reverse('add_event')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Event.objects.count() == 1
    assert Event.objects.get(title='Event Title')
    assert Event.objects.get().title == 'Event Title'
    assert Event.objects.get().description == 'Event Description'
    assert Event.objects.get().start_time.strftime('%Y-%m-%d %H:%M:%S') == '2024-06-16 09:15:00'
    assert Event.objects.get().end_time == datetime.datetime(2024, 6, 16, 10, 15, tzinfo=datetime.timezone.utc)  # this is how it is stored
    assert Event.objects.get().user == user


@pytest.mark.django_db
def test_add_event_get_not_logged():
    client = Client()
    url = reverse('add_event')
    data = {
        'user': 'user',
        'title': 'Event Title',
        'description': 'Event Description',
        'start_time': '2024-06-16 11:15:00',
        'end_time': '2024-06-16 12:15:00'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_add_event_post_missing_data(user):
    client = Client()
    client.force_login(user)
    data = {
        'user': 'user',
        'description': 'Event Description',
        'start_time': '2024-06-16 11:15:00',
        'end_time': '2024-06-16 12:15:00'
    }
    url = reverse('add_event')
    response = client.post(url, data)
    assert response.status_code == 200
    assert Event.objects.count() == 0
    assert "To pole jest wymagane" in response.content.decode()
    data2 = {
        'user': 'user',
        'title': 'Event Title',
        'description': 'Event Description',
        'end_time': '2024-06-16 12:15:00'
    }
    url = reverse('add_event')
    response = client.post(url, data2)
    assert response.status_code == 200
    assert Event.objects.count() == 0
    assert "To pole jest wymagane" in response.content.decode()


@pytest.mark.django_db
def test_add_event_post_empty_field(user):
    client = Client()
    client.force_login(user)
    data = {
        'user': 'user',
        'title': '',
        'description': 'Event Description',
        'start_time': '2024-06-16 11:15:00',
        'end_time': '2024-06-16 12:15:00'
    }
    url = reverse('add_event')
    response = client.post(url, data)
    assert response.status_code == 200
    assert Event.objects.count() == 0
