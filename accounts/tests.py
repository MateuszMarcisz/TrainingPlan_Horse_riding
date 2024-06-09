import pytest
from django.test import TestCase, Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


# Create your tests here.

def test_login_view():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


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
