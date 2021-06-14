import uuid

from django.core.mail import send_mail
from django.db.models import query
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Review, Title
# from .permissions import IsAuthorOrReadOnly
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer
from .models import Review, Title
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User

from .models import Category, Genre, Review, Title
# from .permissions import IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)

class GetPostDelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Title, id=self.kwargs['title_id']).reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=Title.objects.get(id=self.kwargs['title_id']))


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Review, id=self.kwargs['review_id']).comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs['review_id'])
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(GetPostDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class GenreViewSet(GetPostDelViewSet):
    query = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [SearchFilter]
    searh_fields = ['name']


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


@api_view(http_method_names=['POST'])
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
    serializer.save(email=email)
    return Response('Код подтверждения был отправлен Вам на почту.',
                    status=status.HTTP_201_CREATED)
