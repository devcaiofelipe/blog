from django.db import models
from .utils import resize_image
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    post_name = models.CharField(max_length=100)
    post_introduction = models.CharField(max_length=500)
    post_content = models.TextField()
    post_author = models.CharField(max_length=100)
    post_imagem = models.ImageField(upload_to='post_img/img')
    post_creation = models.DateTimeField(auto_now_add=True)
    post_published = models.BooleanField(default=True)
    post_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return self.post_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resize_image(self.post_imagem.name, 800)
