from django.core.mail import send_mail
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, filters, generics
from rest_framework import pagination
from taggit.models import Tag

from core.models import Post, Comment
from core.serializers import PostSerializer, TagSerializer, ContactSerializer, RegisterSerializer, UserSerializer, \
    CommentSerializer


class MainPagePaginator(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class PostViewSet(ModelViewSet):
    search_fields = ['h1', 'title', 'context']
    filter_backends = (filters.SearchFilter, )
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created_at')
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = MainPagePaginator


class TagPostView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = MainPagePaginator

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()


class AsideView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all().order_by('-created_at')[:5]


class FeedbackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            from_email = serializer.validated_data.get('email')
            subject = serializer.validated_data.get('subject')
            message = serializer.validated_data.get('message')
            try:
                send_mail(f'From {name} | {from_email} | {subject}', message, 'dmkrayniy@ukr.net',
                          ['dmkrayniy@ukr.net'])
            except BadHeaderError:
                return Response({"success": "Not valid headers"})
            return Response({'success': 'Sent'})


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User created successfully'
        })


class ProfileView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return post.comments
