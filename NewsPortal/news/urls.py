from django.urls import path, include
# Импортируем созданное нами представление
from .views import *
#from django.views.decorators.cache import cache_page


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_list'),
   #path('', cache_page(60)(PostList.as_view()), name='post_list'),
   # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   #path('news/<int:pk>/', cache_page(5*60)(PostDetail.as_view()), name='post_detail'),
   #path('pages/', include('django.contrib.flatpages.urls')),
   path('news/search/', news_search_f, name='news_search'), # поиск новостей
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('user/upgrade/', upgrade_me, name='upgrade_user'),
   path('user/', include('allauth.urls')),
   path('user/edit/', UserDataUpdate.as_view(), name='user_edit'),
   path('category/<int:cat_id>/subscribe', subscribe_on_cat, name='subscribe'),
   path('category/<int:cat_id>/unsubscribe', unsubscribe_cat, name='unsubscribe'),
   path('category/<int:cat_id>/', show_category, name='category'),
   path('user/stz/', set_timezone, name='set_timezone'),
   #path('news/limit/', news_limit, name='news_limit'),

]