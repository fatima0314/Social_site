from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework import serializers



class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email', 'password' ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            user = UserProfile.objects.create_user(**validated_data)
            return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']



class FollowSerializer(serializers.ModelSerializer):
    follower = UserProfileSimpleSerializer()
    following = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']



class PostSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model =  Post
        fields = ['user','image', 'video']



class PostLikeSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    class Meta:
        model = PostLike
        fields = ['user', 'like', 'created_at']



class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    post = PostSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    class Meta:
        model = PostLike
        fields = ['user', 'post', 'like', 'created_at']



class CommentSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    post = PostSimpleSerializer()
    class Meta:
        model = Comment
        fields = ['user', 'post', 'text']



class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    comment = CommentSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    class Meta:
        model = CommentLike
        fields = ['user', 'comment', 'like', 'created_at']



class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    count_like = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['user', 'text', 'parent','count_like',  'created_at']

    def get_count_like(self, obj):
        return obj.get_count_like()



class StorySerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    class Meta:
        model = Story
        fields = ['user', 'image', 'video', 'created_at']



class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    post_comment = CommentSerializer(many=True, read_only=True)
    post_like = PostLikeSimpleSerializer(many=True, read_only=True)
    count_like = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','user', 'image', 'video', 'description', 'hashtag', 'post_like','post_comment', 'count_like','created_at']

    def get_count_like(self, obj):
        return obj.get_count_like()



class SaveSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Saved
        fields = ['user']



class SaveItemSerializer(serializers.ModelSerializer):
    post = PostSimpleSerializer()
    created_date = serializers.DateTimeField(format='%y-%d-%m  %H:%M')
    class Meta:
        model = SaveItem
        fields = ['post', 'saved', 'created_date']