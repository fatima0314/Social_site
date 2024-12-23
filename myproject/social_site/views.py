from rest_framework import viewsets, generics, status
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import FollowPagination
from .permissions import CheckUser ,CheckFollow
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data,  status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class =LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status = status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs ):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserProfileApiView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class UserProfileEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [CheckUser]


class FollowApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = FollowPagination
    permission_classes = [CheckFollow]



class PostApiView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hashtag']
    ordering_fields = ['created_at']


class PostCreateApiView(generics.CreateAPIView):
    serializer_class = PostSerializer


class PostEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CheckUser]



class PostLikeApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [CheckUser]



class CommentApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CheckUser]


class CommentLikeApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [CheckUser]



class StoryApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [CheckUser]



class SaveItemApiView(generics.ListAPIView):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer