from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentsViewSet,
                    ConfirmationCodeObtainView, CustomTokenObtainPairView,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('v1/reviews', ReviewViewSet, basename='reviews')
router_v1.register('v1/genres', GenreViewSet, basename='genres')
router_v1.register('v1/categories', CategoryViewSet, basename='categories')
router_v1.register('v1/titles', TitleViewSet, basename='titles')
router_v1.register(r'v1/titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register((r'v1/titles/(?P<title_id>\d+)/'
                    r'reviews/(?P<review_id>\d+)/comments'),
                   CommentsViewSet,
                   basename='comments')


urlpatterns = [
    path('',
         include(router_v1.urls)),
    path('v1/auth/email/',
         ConfirmationCodeObtainView.as_view(),
         name='confirmation_code_obtain'),
    path('v1/auth/token/',
         CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
