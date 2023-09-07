from django.core.mail import EmailMultiAlternatives
from celery import shared_task
import time
from django.template.loader import render_to_string
from django.contrib.sites.models import Site # Site.objects.get_current().domain
from django.conf import settings
from datetime import datetime, timedelta
import time
from .models import *

@shared_task
def task_mail_on_post(post_id, user_id):  # задача выслать электронное письмо в html формате при создании новости
    domain = Site.objects.get_current().domain
    # 'https://%s%s' % (Site.objects.get_current().domain, obj.get_absolute_url())
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=user_id)
    path = post.get_absolute_url()
    html_content = render_to_string(
        'mail/new_post.html',
        {
            'username': user.username,  # получение имени пользователя
            'message': post.text[:50] + '...', # 50 символов текста статьи
            'post_url': f'http://{domain}{path}', # формирование url поста
        }
    )
    # формирование письма
    msg = EmailMultiAlternatives(
        subject=f'{post.header}', # тема письма
        body=post.text[:50] + '...', # тело
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],  # это то же, что и recipients_list
        # берем email пользователя
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

