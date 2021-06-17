from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


def year_validator(value):
    if value < 1000 or value > datetime.now().year:
        raise ValidationError(f'{value}s is not correct year!')


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=100)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=100)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.IntegerField(verbose_name='Год выхода',
                               validators=[year_validator])
    description = models.CharField(verbose_name='Описание', max_length=600,
                                   default="Описание отсутсвует")
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 related_name='category', blank=True,
                                 null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, verbose_name='Жанр',
                              related_name='genre', blank=True, null=True,
                              on_delete=models.SET_NULL)
    rating = models.IntegerField(verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор отзыва',
                               on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title, verbose_name='Название объекта',
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(validators=[MaxValueValidator(10),
                                            MinValueValidator(1)])
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created',)

    def __str__(self):
        return (
            f'Автор отзыва: {self.author.username}, '
            f'Текст: {self.text[:20]}, '
            f'Дата: {self.created}, '
            f'Оценка: {self.score}'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return (
            f'Автор: {self.author.username}, '
            f'Название: {self.title}, '
            f'Текст: {self.text[:20]}, '
            f'Дата: {self.created}'
        )
