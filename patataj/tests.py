import pytest
from django.test import TestCase, Client
from django.urls import reverse

from patataj.models import Training


# Create your tests here.

def test_home_page():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_training_list(trainings):
    client = Client()
    url = reverse('training_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['page_object'].object_list) == 5  # bo tyle mamy w pagination
    paginator = response.context['page_object'].paginator
    assert paginator.num_pages == 3  # sprawdzamy, czy jest mamy 15 treningów to będzie 5 list
    assert paginator.count == len(trainings)  # tu sprawdzamy, czy faktycznie jest ich tyle samo
    response_page_2 = client.get(url, {'page': 2})  # patrzymy czy druga strona istnieje
    assert response_page_2.status_code == 200


@pytest.mark.django_db
def test_training_list_handles_out_of_range_page_number(trainings):
    client = Client()
    url = reverse('training_list')
    response = client.get(url, {'page': 999})
    assert response.status_code == 200
    response = client.get(url, {'page': 0})
    assert response.status_code == 200
    paginator = response.context['page_object'].paginator
    assert paginator.num_pages == 3


@pytest.mark.django_db
def test_training_detail(training):
    client = Client()
    url = reverse('training_detail', args=(training.id,))
    response = client.get(url)
    assert response.status_code == 200
    training_context = response.context['training']
    assert training_context == training

    content = response.content.decode()
    assert training.name in content
    assert training.description in content
    assert str(training.length) in content


