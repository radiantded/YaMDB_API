import uuid

from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User
from .permissions import IsAdminOrReadOnly
from .models import Category, Genre, Review, Title
from .permissions import IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer, CustomTokenObtainPairSerializer)


class GetPostDelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Title, id=self.kwargs['title_id']).reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=Title.objects.get(id=self.kwargs['title_id']))


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Review, id=self.kwargs['review_id']).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs['review_id'])
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(GetPostDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']


class GenreViewSet(GetPostDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,]


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
    message = 'Ваш код подтверждения: {confirmation_code}'
    confirmation_code = uuid.uuid4()
    send_mail(message_subject,
              message.format(
                  confirmation_code=confirmation_code
              ),
              DEFAULT_FROM_EMAIL,
              [email])
    if not User.objects.filter(username=email, email=email).exists():
        serializer.save(username=email,
                        email=email,
                        confirmation_code=confirmation_code)
        return Response('Код подтверждения был отправлен Вам на почту.',
                        status=status.HTTP_201_CREATED)
