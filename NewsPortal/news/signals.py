from django.shortcuts import render
from django.utils import timezone
from requests import request

from .models import *
from .tasks import *
from django.template.loader import render_to_string
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives


@receiver(m2m_changed, sender=Post.categories.through)
# m2m_changed возникает при изменении ManyToManyField модели.
def send_mail_on_post(sender, action, instance, **kwargs):
    # отправляем письмо
    if action == 'post_add':  # если событие добавление поста
        cats = instance.categories.all()  # берем все категории
        for c in cats:  # цикл по всем категориям
            users = c.subscribers.all()  # бежим по связям, пользователей, которые подписаны на категории новостей, собираем этих пользователей
            for u in users:
                task_mail_on_post.delay(instance.pk, u.pk)  # рассылка писем


# @receiver(post_save, sender=Post)
# def day_news_limit(sender, instance, **kwargs):
#     user = instance.author.Author_User
#     today = timezone.now().date()
#     count = Post.objects.filter(Author__User=user, date__create=today).count()
#     text = 'Больше трех статей в сутки создавать одному автору запрещено!'
#     return render(request, 'user/post_limit.html', {'text': text})
