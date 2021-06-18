from django.contrib.auth.models import AbstractUser
from django.db import models

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
        unique=True
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
    confirmation_code = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'Username: {self.username}, '
                f'адрес электронной почты: {self.email}, '
                f'роль: {self.role}')
