from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name',
                    'username', 'bio', 'email',
                    'role', 'confirmation_code')
    search_fields = ('username', 'email', 'role')
    list_filter = ('username', 'role')
    empty_value_display = '-пусто-'
