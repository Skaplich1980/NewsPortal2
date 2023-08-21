from django.urls import path, include
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_list'),
   # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   #path('pages/', include('django.contrib.flatpages.urls')),
   path('news/search/', news_search_f, name='news_search'), # поиск новостей
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]