from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import ReviewSerializer, CommentSerializer, UserSerializer
from .models import Review, Titles
from users.models import User


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Titles, id=self.kwargs['title_id']).comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Titles, id=self.kwargs['title_id'])
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(http_method_names=['POST'])
def send_email(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email_address = serializer.validated_data['email']
        send_mail('Confirmation code for YaMDb',
                  'l,km0-i9jio', 'sss',
                  [email_address])
        return Response(serializer.data, status=status.HTTP_200_OK)
    raise ValidationError('Проверьте адрес электронной почты')
