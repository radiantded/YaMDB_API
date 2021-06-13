from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (ReviewViewSet,
                    CommentsViewSet,
                    UserViewSet,
                    send_email)

router_v1 = routers.DefaultRouter()
router_v1.register('v1/users',
                   UserViewSet,
                   basename='users')
router_v1.register('v1/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'v1/reviews/(?P<title_id>\d+)/comments',
                   CommentsViewSet,
                   basename='comments')


urlpatterns = [
    path('',
         include(router_v1.urls)),
    path('v1/auth/email/',
         send_email),
    path('v1/auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
