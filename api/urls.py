from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import ReviewViewSet, CommentsViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('v1/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'v1/reviews/(?P<title_id>\d+)/comments',
                   CommentsViewSet,
                   basename='comments')


urlpatterns = [
    path('', include(router_v1.urls)),
]
