from datetime import datetime

import pytest
from django.utils import timezone

from todo.models import ToDo
from todo.tests.fixtures import create_tasks, create_users
from todo.tests.utils import get, post, delete


@pytest.mark.django_db
def test_list_tasks_for_user_authenticated(create_tasks, create_users):

    # Total Tasks
    assert ToDo.objects.count() == 5

    debianitram, amarello = create_users
    response = get('/api/v1/todo/', user_logged=debianitram)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    response = get('/api/v1/todo/', user_logged=amarello)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.django_db
def test_list_tasks_failed_user_not_authenticated(create_tasks):
    response = get('/api/v1/todo/')
    assert response.status_code == 403      # Forbidden.


@pytest.mark.django_db
def test_create_task(create_users):
    debianitram, _ = create_users
    TODO_CONTENT = 'Wash the dog.'
    response = post('/api/v1/todo/', data={'content': TODO_CONTENT}, user_logged=debianitram)
    assert response.status_code == 201
    assert ToDo.objects.filter(content=TODO_CONTENT).exists() is True


@pytest.mark.django_db
def test_delete_task(create_tasks, create_users):
    _, amarello = create_users
    tasks = ToDo.objects.filter_by_user(amarello)

    assert tasks.count() == 2
    last_task = tasks.last()
    response = delete(f'/api/v1/todo/{last_task.pk}', user_logged=amarello)
    assert response.status_code == 204
    assert ToDo.objects.filter_by_user(amarello).count() == 1


@pytest.mark.django_db
def test_fails_to_delete_task_another_user(create_tasks, create_users):
    debianitram, amarello = create_users
    last_task_amarello = ToDo.objects.filter_by_user(amarello).last()

    response = delete(f'/api/v1/todo/{last_task_amarello.pk}', user_logged=debianitram)
    assert response.status_code == 404      # Not found.


@pytest.mark.django_db
def test_mark_tasks_as_completed(create_tasks, create_users):
    debianitram, _ = create_users
    tasks_debianitram = ToDo.objects.filter_by_user(debianitram)
    assert tasks_debianitram.filter_completed().count() == 0

    list_tasks_id = list(tasks_debianitram.values_list('id', flat=True))
    data = {'tasks_id': list_tasks_id}
    response = post('/api/v1/todo/mark_as_completed/', data=data, user_logged=debianitram)
    assert response.status_code == 200
    data = response.json()
    assert data['count_tasks_completed'] == 3
    assert ToDo.objects.filter_by_user(debianitram).filter_completed().count() == 3


@pytest.mark.django_db
def test_mark_tasks_as_completed_only_user_authenticated(create_tasks, create_users):
    _, amarello = create_users
    all_tasks = ToDo.objects.all()
    assert all_tasks.filter_completed().count() == 0
    assert all_tasks.count() == 5

    list_tasks_id = list(all_tasks.values_list('id', flat=True))
    data = {'tasks_id': list_tasks_id}
    response = post('/api/v1/todo/mark_as_completed/', data=data, user_logged=amarello)
    assert response.status_code == 200
    data = response.json()
    assert data['count_tasks_completed'] == 2
    assert ToDo.objects.all().filter_completed().count() == 2


@pytest.mark.django_db
def test_filter_by_content(create_tasks, create_users):
    debianitram, _ = create_users
    response = get('/api/v1/todo/?content=invera', user_logged=debianitram)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['content'] == 'Download challenge Invera'


@pytest.mark.django_db
def test_filter_by_created_on(create_tasks, create_users, mocker):
    debianitram, _ = create_users

    mocker.patch.object(timezone, 'now')
    timezone.now.return_value = datetime(2021, 3, 14, 12, 0, 0, tzinfo=timezone.utc)

    ToDo.objects.create(
        content="buy cake for Nina's birthday",
        created_by=debianitram
    )

    response = get('/api/v1/todo/?created_on=2021-03-14', user_logged=debianitram)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['content'] == "buy cake for Nina's birthday"
    assert '2021-03-14' in data[0]['created_on']
