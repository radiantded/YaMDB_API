import uuid

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Review, Title
# from .permissions import IsAuthorOrReadOnly
from .serializers import CustomTokenObtainPairSerializer, ReviewSerializer, CommentSerializer, UserSerializer
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Title, id=self.kwargs['title_id']).comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs['title_id'])
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
def send_email(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data['email']
    message_subject = 'Код подтверждения YaMDb'
    confirmation_code = 'Ваш код подтверждения: {confirmation_code}'
    random_code = uuid.uuid4()
    send_mail(message_subject,
              confirmation_code.format(
                  confirmation_code=random_code
              ),
              DEFAULT_FROM_EMAIL,
              [email])
    if not User.objects.filter(username=email, email=email).exists():
        serializer.save(username=email,
                        email=email,
                        confirmation_code=random_code)
        return Response('Код подтверждения был отправлен Вам на почту.',
                        status=status.HTTP_201_CREATED)
