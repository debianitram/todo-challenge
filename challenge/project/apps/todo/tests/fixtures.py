import pytest
from django.contrib.auth import get_user_model

from todo.models import ToDo

User = get_user_model()


@pytest.fixture
def create_users():
    debianitram, _ = User.objects.get_or_create(
        username='debianitram',
        email='debianitram@gmail.com',
        defaults={
            'first_name': 'Martín',
            'last_name': 'Miranda',
        }
    )

    debianitram.set_password('password_very_secret')
    debianitram.save(update_fields=('password', ))

    amarello, _ = User.objects.get_or_create(
        username='amarello',
        email='adrianmarello@gmail.com',
        defaults={
            'first_name': 'Adrian',
            'last_name': 'Marello'
        }
    )

    return debianitram, amarello


@pytest.fixture
def create_tasks(create_users):
    debianitram, amarello = create_users

    ToDo.objects.get_or_create(content='Download challenge Invera', created_by=debianitram)
    ToDo.objects.get_or_create(content='Buy a welding machine in Mercado Libre', created_by=debianitram)
    ToDo.objects.get_or_create(content='To study English!', created_by=debianitram)

    ToDo.objects.get_or_create(content='Call Martín.', created_by=amarello)
    ToDo.objects.get_or_create(content='Talk to Martín about the new project.', created_by=amarello)


