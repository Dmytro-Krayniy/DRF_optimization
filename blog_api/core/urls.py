from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views
from core.views import PostViewSet, ProfileView, CommentView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', views.TagView.as_view(), name='tags'),
    path('tags/<slug:tag_slug>/', views.TagPostView.as_view(), name='posts_by_tag'),
    path('aside/', views.AsideView.as_view()),
    path('feedback/', views.FeedbackView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<slug:post_slug>/', CommentView.as_view()),
]
