from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.


class Comment(models.Model):
    comment_content = models.CharField(max_length=300)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_creation = models.DateField(auto_now_add=True)
    comment_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-comment_creation']
