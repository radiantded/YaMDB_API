import secrets

from rest_framework_simplejwt.serializers import RefreshToken

from .models import User


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def create_username(email):
    def check_username(username):
        if not User.objects.filter(username=username).exists():
            return username
        return check_username(f'{username}_{secrets.token_hex(6)}')
    return check_username(email.split('@')[0])
