import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains


# Create your tests here.

def test_login_view():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_wrong_password(user):
    client = Client()
    url = reverse('login')
    response = client.post(url, {'username': user.username, 'password': 'inne hasło'})
    assert response.status_code == 200
    assertContains(response, reverse('login'))
    assertContains(response, "Nieprawidłowa nazwa użytkownika lub hasło")
    assert 'error' in response.context
    assert response.context['error'] == "Nieprawidłowa nazwa użytkownika lub hasło"


def test_logout_view():
    client = Client()
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302


def test_create_user_view_get():
    client = Client()
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'accounts/create_user.html')


@pytest.mark.django_db
def test_create_user_view_post():
    client = Client()
    url = reverse('register')
    data = {
        'username': 'test',
        'password': 'test password',
        'password2': 'test password'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.get(username='test')


@pytest.mark.django_db
def test_create_user_view_post_wrong():
    client = Client()
    url = reverse('register')
    data = {
        'username': 'test',
        'password': 'test password',
        'password2': 'test prd'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assertContains(response, "Hasła nie są zgodne")
