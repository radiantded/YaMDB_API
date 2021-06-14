from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
    ('django admin', 'администратор Django')
)


class User(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    username = models.CharField(
        max_length=128,
        unique=True,
        blank=True,
        null=True
    )
    bio = models.TextField(
        max_length=1000,
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True
    )
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'Имя: {self.first_name}, '
                f'фамилия: {self.last_name}, '
                f'о себе: {self.bio[:15]}, '
                f'username: {self.username}, '
                f'адрес электронной почты: {self.email}, '
                f'роль: {self.role}')
