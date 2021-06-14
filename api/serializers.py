from rest_framework import serializers, validators

from .models import Review, Comment, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    score = serializers.IntegerField(
        max_value=10,
        min_value=1
    )

    class Meta:
        model = Review
        fields = '__all__'
        required_fields = ('text', 'score',)
        # validators = [
        #     validators.UniqueTogetherValidator(
        #         queryset=Title.objects.all(),
        #         fields=('author'),
        #         message='Низя'
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        required_fields = ('text',)
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'bio', 'email', 'role']
