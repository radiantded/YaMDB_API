from django.urls import path, include
from rest_framework import routers

from .views import ReviewViewSet, CommentsViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('v1/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'v1/posts/(?P<title_id>\d+)/comments',
                   CommentsViewSet,
                   basename='comments')


urlpatterns = [
    path('', include(router_v1.urls)),
]
