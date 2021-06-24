import secrets

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (
    IsAdmin, IsAdminOrReadOnly,
    IsAuthorOrModeratorOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentSerializer,
    ConfirmationDataSerializer, EmailSerializer,
    GenreSerializer, ReviewSerializer,
    TitleReadSerializer, TitleWriteSerializer,
    UserSerializer
)
from .utils import create_username, get_token


class CategoryAndGenreBaseClass(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrReadOnly,
    ]

    def get_queryset(self):
        return get_object_or_404(Title,
                                 id=self.kwargs.get('title_id')).reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        title=title)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrReadOnly,
    ]

    def get_queryset(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']
    permission_classes = [IsAdmin]

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CategoryAndGenreBaseClass):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreBaseClass):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, ]
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend, ]
    search_fields = ['category', 'genre', 'name', 'year']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = ConfirmationDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        email=serializer.validated_data['email'].lower(),
        confirmation_code=serializer.validated_data['confirmation_code']
    )
    data = get_token(user)
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_email(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email'].lower()
    message_subject = 'YaMDb confirmation code'
    message = 'Ваш код подтверждения: {confirmation_code}'
    confirmation_code = secrets.token_hex()
    send_mail(
        message_subject,
        message.format(
            confirmation_code=confirmation_code),
        DEFAULT_FROM_EMAIL,
        [email]
    )
    user, created = User.objects.update_or_create(
        email=email,
        defaults={
            'confirmation_code': confirmation_code,
            'username': create_username(email)
        }
    )
    if created:
        return Response(
            'Код подтверждения был отправлен Вам на почту.',
            status=status.HTTP_201_CREATED)
    return Response(
        'Новый код подтверждения был отправлен Вам на почту.',
        status=status.HTTP_200_OK)
