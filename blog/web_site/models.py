from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Создание своих моделек.

"""
create table if not exists category(
    name 
)
"""


class Category(models.Model):
    name = models.CharField(max_length=155, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(verbose_name="Заголовок статьи", max_length=155, unique=True)
    short_description = models.TextField(verbose_name="Краткое описание", max_length=300)
    full_description = models.TextField(verbose_name="Полное описание")
    photo = models.ImageField(verbose_name="Фото", upload_to="photos/articles/")
    views = models.IntegerField(verbose_name="Количество просмотров", default=0)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="articles")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="articles")

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_id': self.pk})


class ArticleCountView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=150)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    body = models.TextField()


class Like(models.Model):
    user = models.ManyToManyField(User, related_name="likes")
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)


class DisLike(models.Model):
    user = models.ManyToManyField(User, related_name="dislikes")
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)