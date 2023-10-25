from django.db import models
from django.contrib.auth.models import User
from params import *
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
#from django.core.cache import cache

news = 'NS'
article = 'AR'

POST_TYPES = [
    (news, 'Новость'),
    (article, 'Статья'),
]

class Post(models.Model): # статьи и новости, которые создают пользователи
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Author

    #  удаление header = models.CharField(max_length=255) - title поле
    # заголовок публикации

    categoryType = models.CharField(max_length=80, choices=POST_TYPES, default=news)
    # поле с выбором — «статья» или «новость», по умолчанию статья
    # CATEGORY_CHOISES описан в файле параметров params

    date_create=models.DateTimeField(auto_now_add=True)
    # автоматически добавляемая дата и время создания

    categories = models.ManyToManyField('Category', through='PostCategory')
    #categories = models.ManyToManyField(Category, through='PostCategory')  # категории публикаций
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)

    title =models.CharField(max_length=150)
    # заголовок статьи/новости

    show_title = models.CharField(max_length=100)
    # отображение в шаблонах

    text=models.TextField()
    # текст статьи/новости

    rating=models.SmallIntegerField(default=0)
    # рейтинг статьи/новости

    def like(self):
        self.rank+=1
        self.save

    def dislike(self):
        self.rank -= 1
        self.save

    def preview(self): # предварительный просмотр публикации
        return self.text[0:128]+'...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
    #     cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Post;

    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);

    text = models.TextField()
    # текст комментария;

    date_create = models.DateTimeField(auto_now_add=True)
    # дата и время создания комментария;

    rating   = models.SmallIntegerField(default=0)
    # рейтинг комментария.

    def like(self):
        self.rank+=1
        self.save

    def dislike(self):
        self.rank -= 1
        self.save

    def __str__(self):
        return self.text()[0:20]

class Author(models.Model):
    Author_User = models.OneToOneField(User, on_delete=models.CASCADE)
    # связь один ко одному встроенной моделью пользователей User
    rating = models.SmallIntegerField(default=0)
    # рейтинг пользователя

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3;
        # суммарный рейтинг всех комментариев автора;
        # суммарный рейтинг всех комментариев к статьям автора.
        author_post_rating = Post.objects.filter(author_id=self.pk).aggregate(r1=Coalesce(Sum('rating'),0))['r1']
        author_comments_rating = Comment.objects.filter(user_id=self.user).aggregate(r2=Coalesce(Sum('rating'),0))['r2']
        author_post_commits_rating = Comment.objects.filter(post__author__user=self.user).aggregate(r3=Coalesce(Sum('rating'),0))['r3']
        self.rating=author_post_rating*3+author_comments_rating+author_post_commits_rating
        self.save

class Category(models.Model): # Категории новостей/статей
    name = models.CharField(max_length=255, unique=True, db_index=True)  # название категории, уникальное поле
    subscribers = models.ManyToManyField(User, through='SubscribersCategory')  # категории публикаций

    def __str__(self):
        return self.name  #return self.name.title()

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})


class PostCategory(models.Model): # Промежуточная модель для связи «многие ко многим»w

    postLink = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Post

    CategoryLink = models.ForeignKey(Category, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Category


class SubscribersCategory(models.Model):   # промежуточная таблица для связи много-к-многим
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)     # ид пользователя
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)     # ид категории


