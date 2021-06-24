from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'пользователь'),
    (MODERATOR, 'модератор'),
    (ADMIN, 'админ')
)


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя', max_length=30, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=30, blank=True, null=True
    )
    username = models.CharField(
        verbose_name='Ник', max_length=128, unique=True
    )
    bio = models.TextField(
        verbose_name='О себе', max_length=1000, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты', unique=True
    )
    role = models.CharField(
        verbose_name='Роль', max_length=30, choices=ROLES, default=USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения', max_length=100,
        null=True, blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'Username: {self.username}, '
                f'адрес электронной почты: {self.email}, '
                f'роль: {self.role}')


def year_validator(value):
    if not (1000 < value <= datetime.now().year):
        raise ValidationError(f'"{value}" некорректное значение года!')


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=100)
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор категории', max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=100)
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор жанра', max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.IntegerField(
        verbose_name='Год выхода', validators=[year_validator]
    )
    description = models.CharField(
        verbose_name='Описание', max_length=600, null=True, blank=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория', related_name='titles',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанры', related_name='titles', blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор отзыва', on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title, verbose_name='Произведение', on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, message='Максимальное значение - 10'),
            MinValueValidator(1, message='Минимальное значение - 1')],
        help_text=('Введите значение от 1 до 10'))
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            f'Автор отзыва: {self.author.username}, '
            f'Текст: {self.text[:20]}, '
            f'Дата: {self.pub_date}, '
            f'Оценка: {self.score}'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор комментария', on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, verbose_name='Отзыв', on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            f'Автор: {self.author.username}, '
            f'Текст: {self.text[:20]}, '
            f'Дата: {self.pub_date}'
        )
