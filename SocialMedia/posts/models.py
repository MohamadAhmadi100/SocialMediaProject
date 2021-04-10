from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=800)
    slug = models.SlugField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body[:40]}"

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.created.year, self.created.month, self.created.day, self.slug])

    class Meta:
        ordering = ('-created',)

    def likes_count(self):
        return self.post_like.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='u_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='p_comment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='r_comment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"

    class Meta:
        ordering = ('-created',)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')

    def __str__(self):
        return f"{self.user} liked{self.post.slug}"
