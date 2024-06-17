import datetime

import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from kalendarz.forms import EventForm
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
def test_add_event_get_initial_data(user):
    client = Client()
    client.force_login(user)
    date = '2024-06-16'
    url = reverse('add_event') + f'?date={date}'
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, EventForm)


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


@pytest.mark.django_db
def test_event_detail(event):
    client = Client()
    url = reverse('event_detail', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 200
    event_context = response.context['event']
    assert event_context == event
    content = response.content.decode('utf-8')
    assert event.title in content
    assert event.description in content


@pytest.mark.django_db
def test_event_edit_get(event, user):
    client = Client()
    client.force_login(user)
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert Event.objects.count() == 1
    assert Event.objects.get(title='Event Title')


@pytest.mark.django_db
def test_event_edit_get_not_logged(event):
    client = Client()
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_event_edit_get_wrong_user(event, user):
    client = Client()
    user2 = User.objects.create_user(username='user2', password='<PASSWORD>')
    client.force_login(user2)
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 403
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_event_edit_post(event, user):
    client = Client()
    client.force_login(user)
    data = {
        'title': 'Event Title2',
        'description': 'Event Description2',
        'start_time': '2024-06-16T11:15:00',
        'end_time': '2024-06-16T12:15:00',
    }
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.post(url, data)
    # assert 'error' in response.content.decode('utf-8').lower()
    # print(response.content.decode('utf-8'))
    assert response.status_code == 302
    edited_event = Event.objects.get(pk=event.pk)
    assert edited_event.title == data['title']
    assert edited_event.title == 'Event Title2'
    assert edited_event.description == data['description']
    assert edited_event.user == user


@pytest.mark.django_db
def test_event_edit_post_empty_field(event, user):
    client = Client()
    client.force_login(user)
    data = {
        'title': '',
        'description': 'Event Description2',
        'start_time': '2024-06-16T11:15:00',
        'end_time': '2024-06-16T12:15:00',
    }
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.content.decode()


@pytest.mark.django_db
def test_event_edit_post_wrong_user(event, user):
    client = Client()
    user2 = User.objects.create_user(username='user2', password='<PASSWORD>')
    client.force_login(user2)
    data = {
        'title': '',
        'description': 'Event Description2',
        'start_time': '2024-06-16T11:15:00',
        'end_time': '2024-06-16T12:15:00',
    }
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_event_edit_post_not_logged(event):
    client = Client()
    data = {
        'title': 'Event Title2',
        'description': 'Event Description2',
        'start_time': '2024-06-16T11:15:00',
        'end_time': '2024-06-16T12:15:00',
    }
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.post(url, data)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_event_edit_post_missing_field(event, user):
    client = Client()
    client.force_login(user)
    data = {
        'title': 'Event Title2',
        'description': 'Event Description2',
        'end_time': '2024-06-16T12:15:00',
    }
    url = reverse('event_edit', kwargs={'pk': event.pk})
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'To pole jest wymagane' in response.content.decode()


@pytest.mark.django_db
def test_event_delete_get(event, user):
    client = Client()
    client.force_login(user)
    url = reverse('event_delete', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_event_delete_get_not_logged(event):
    client = Client()
    url = reverse('event_delete', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_event_delete_get_wrong_user(event, user):
    client = Client()
    user2 = User.objects.create_user(username='user2', password='<PASSWORD>')
    client.force_login(user2)
    url = reverse('event_delete', kwargs={'pk': event.pk})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_event_delete_post(event, user):
    client = Client()
    client.force_login(user)
    url = reverse('event_delete', args=(event.id,))
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert not Event.objects.filter(id=event.id).exists()
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_event_delete_post_wrong_user(event, user):
    client = Client()
    user2 = User.objects.create_user(username='user2', password='<PASSWORD>')
    client.force_login(user2)
    url = reverse('event_delete', args=(event.id,))
    response = client.post(url, follow=True)
    assert response.status_code == 403
