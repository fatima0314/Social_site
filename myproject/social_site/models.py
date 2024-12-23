from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bio = models.TextField()
    image = models.ImageField(upload_to='user_images/')
    website = models.URLField()

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete= models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}-{self.following}'

    class Meta:
        unique_together = ('follower', 'following',)


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos', null=True, blank=True)
    description = models.TextField()
    hashtag = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_count_like(self):
        likes = self.post_like.all()
        if likes.exists():
            return likes.count()
        return 0


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post',)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_count_like(self):
        likes = self.comment_like.all()
        if likes.exists():
            return likes.count()
        return 0


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment',)


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)
    video = models.FileField(upload_to='story_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Saved(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved = models.ForeignKey(Saved, on_delete=models.CASCADE , related_name='saved')
    created_date = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    video = models.FileField(upload_to='message_videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)