from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CategoryViewSet, CommentsViewSet,
    GenreViewSet, ReviewViewSet,
    TitleViewSet, UserViewSet,
    obtain_token, send_email
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/',
         include(router_v1.urls)),
    path('v1/auth/email/',
         send_email),
    path('v1/auth/token/',
         obtain_token),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
