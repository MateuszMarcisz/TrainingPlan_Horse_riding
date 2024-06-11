import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from patataj import models
from patataj.models import Training, Plan


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
def test_training_list_filtering_for_element(trainings):
    client = Client()
    url = reverse('training_list')
    response = client.get(url, {'name': '14'})
    assert response.status_code == 200
    assert len(response.context['page_object'].object_list) == 1


@pytest.mark.django_db
def test_training_list_filtering_for_multiple_element(trainings):
    client = Client()
    url = reverse('training_list')
    response = client.get(url, {'name': 'training'})
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


@pytest.mark.django_db
def test_delete_training_exists(training):
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    url = reverse('training_delete', args=(training.id,))
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_training_works_properly(training):
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    url = reverse('training_delete', args=(training.id,))
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert not Training.objects.filter(id=training.id).exists()


@pytest.mark.django_db
def test_add_training_get():
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    url = reverse('training_add')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_training_get_without_login():
    client = Client()
    url = reverse('training_add')
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_add_training_post():
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    data = {
        'name': 'Skoki w boki',
        'training_type': 'SK',
        'description': 'Skoki w boki opisane',
        'length': '84'
    }
    url = reverse('training_add')
    # models.Training.objects.create(name=data['name'], type=data['training_type'], description=data['description'],
    #                                length=data['length'])
    # tutaj miałem błąd w tym teście i powyższe było do sprawdzania, czy w ogóle moje dane mogą być zapisane do db
    initial_count = Training.objects.count()
    response = client.post(url, data)
    assert response.status_code == 302
    assert Training.objects.count() == initial_count + 1
    assert Training.objects.get(name='Skoki w boki')
    assert Training.objects.get().name == 'Skoki w boki'


@pytest.mark.django_db
def test_add_training_post_empty_data():
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    data = {
        'name': 'Skoki w boki',
        'training_type': 'SK',
        'description': '',
        'length': '84'
    }
    url = reverse('training_add')
    response = client.post(url, data)
    assert response.status_code == 200
    assert not Training.objects.exists()


@pytest.mark.django_db
def test_add_training_post_wrong_data():
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    data = {
        'nam111e': 'Skoki w boki',
        'training_type': 'SK',
        'description': 'hehehhe',
        'length': '84'
    }
    url = reverse('training_add')
    response = client.post(url, data)
    assert response.status_code == 200
    assert not Training.objects.exists()


@pytest.mark.django_db
def test_add_training_post_missing_data():
    client = Client()
    test_user = User.objects.create_user(username='testuser', password='password')
    client.force_login(test_user)
    data = {
        'name': 'Skoki w boki',
        'training_type': 'SK',
        'description': 'hehehhe',
    }
    url = reverse('training_add')
    response = client.post(url, data)
    assert response.status_code == 200
    assert not Training.objects.exists()


@pytest.mark.django_db
def test_training_edit_get(training, user):
    client = Client()
    client.force_login(user)
    url = reverse('training_edit', args=(training.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert Training.objects.filter(id=training.id).exists()
    assert Training.objects.get(name='name')


@pytest.mark.django_db
def test_training_edit_post(training, user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'New Training Name',
        'training_type': 'SK',
        'description': 'New Training Description',
        'length': '100',
    }
    url = reverse('training_edit', args=(training.id,))
    response = client.post(url, data)
    assert response.status_code == 302
    edited_training = Training.objects.get(pk=training.id)
    assert edited_training.name == 'New Training Name'


@pytest.mark.django_db
def test_training_edit_post_empty_data(training, user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'New Training Name',
        'training_type': 'SK',
        'description': '',
        'length': '100',
    }
    url = reverse('training_edit', args=(training.id,))
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_training_edit_post_empty_data(training, user):
    client = Client()
    client.force_login(user)
    data1 = {
        'name': 'New Training Name',
        'description': 'fghff',
        'length': '100',
    }
    url = reverse('training_edit', args=(training.id,))
    response = client.post(url, data1)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_list(plans, user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['page_object'].object_list) == 5
    paginator = response.context['page_object'].paginator
    assert paginator.num_pages == 3
    assert paginator.count == len(plans)
    response_page_2 = client.get(url, {'page': 2})
    assert response_page_2.status_code == 200


@pytest.mark.django_db
def test_plan_list_no_login(plans):
    client = Client()
    url = reverse('plan_list')
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'



@pytest.mark.django_db
def test_plan_list_filtering_for_element(plans, user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_list')
    response = client.get(url, {'name': '14'})
    assert response.status_code == 200
    assert len(response.context['page_object'].object_list) == 1


@pytest.mark.django_db
def test_plan_detail(plan, user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_detail', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 200
    plan_context = response.context['plan']
    assert plan_context == plan
    content = response.content.decode()
    assert plan.name in content
    assert plan.description in content


@pytest.mark.django_db
def test_plan_detail_not_logged(plan):
    client = Client()
    url = reverse('plan_detail', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_plan_detail_wrong_user(plan):
    client = Client()
    user2 = User.objects.create_user(username='testuser', password='password', id=2)
    client.force_login(user2)
    url = reverse('plan_detail', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 403  # bo denied


@pytest.mark.django_db
def test_add_plan_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_add')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_plan_get_without_login():
    client = Client()
    url = reverse('plan_add')
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_add_plan_post(user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'Weekend w Bieszczadach',
        'description': 'Grill i piwo',
    }
    url = reverse('plan_add')
    initial_count = Plan.objects.count()
    response = client.post(url, data)
    assert response.status_code == 302
    assert Plan.objects.count() == initial_count + 1
    assert Plan.objects.get(name='Weekend w Bieszczadach')
    assert Plan.objects.get().name == 'Weekend w Bieszczadach'


@pytest.mark.django_db
def test_add_plan_post_missing_data(user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'Weekend w Bieszczadach',
    }
    url = reverse('plan_add')
    response = client.post(url, data)
    assert response.status_code == 200
    assert Plan.objects.count() == 0


@pytest.mark.django_db
def test_add_plan_post_empty_field(user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'Weekend w Bieszczadach',
        'description': '',
    }
    url = reverse('plan_add')
    response = client.post(url, data)
    assert response.status_code == 200
    assert Plan.objects.count() == 0
    assert 'Opis wymagany!' in response.content.decode()  # prosty sposób na wyświetlenie czy dana treść istnieje


@pytest.mark.django_db
def test_plan_edit_get(plan, user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_edit', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert Plan.objects.filter(id=plan.id).exists()
    assert Plan.objects.get(name='name')


@pytest.mark.django_db
def test_plan_edit_get_wrong_user(plan):
    client = Client()
    user2 = User.objects.create_user(username='testuser', password='password', id=2)
    client.force_login(user2)
    url = reverse('plan_edit', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_plan_edit_post(plan, user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'New Plan Name',
        'description': 'New Plan Description',
        'user_id': user.id,
    }
    url = reverse('plan_edit', args=(plan.id,))
    response = client.post(url, data)
    assert response.status_code == 302
    edited_plan = Plan.objects.get(pk=plan.id)
    assert edited_plan.name == 'New Plan Name'


@pytest.mark.django_db
def test_plan_edit_post_empty_data(training, user):
    client = Client()
    client.force_login(user)
    data = {
        'name': 'New Training Name',
        'description': '',
    }
    url = reverse('training_edit', args=(training.id,))
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'Opis wymagany!' in response.content.decode()






@pytest.mark.django_db
def test_delete_plan_get(plan, user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_delete', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_plan_get_no_user(plan):
    client = Client()
    url = reverse('plan_delete', args=(plan.id,))
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f'{login_url}?next={url}'


@pytest.mark.django_db
def test_delete_plan_works_properly(plan, user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_delete', args=(plan.id,))
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert not Plan.objects.filter(id=plan.id).exists()
