from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'first_name',
        'last_name', 'username',
        'bio', 'email', 'role',
        'confirmation_code'
    )
    search_fields = ('username', 'email', 'role')
    list_filter = ('role',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'score', 'pub_date')
    search_fields = ('author', 'title', 'score', 'pub_date',)
    list_filter = ('author', 'score', 'title', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review', 'pub_date')
    search_fields = ('author', 'review', 'pub_date',)
    list_filter = ('author', 'review', 'pub_date',)
    empty_value_display = '-пусто-'
