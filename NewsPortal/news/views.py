from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
import pytz
from django.utils.translation import gettext as _
from django.utils import timezone
from .models import POST_TYPES, news as string_news, article as string_article



paginator_count = 10 # вынесли константу для использования в нескольких местах кода
# кол-во отображаемых на страніце новостей

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news/posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = paginator_count  # вот так мы можем указать количество записей на странице

    #Переопределяем функцию получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельномой новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'news/post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

def news_search_f(request):
    queryset = Post.objects.all()
    filterset = NewsFilter(request.GET, queryset)
    page = request.GET.get('page')
    paginator = Paginator(filterset.qs, paginator_count)
    try:
        filter_qs = paginator.get_page(page)
    except PageNotAnInteger:
        filter_qs = paginator.get_page(paginator_count)
    except EmptyPage:
        filter_qs = paginator.get_page(paginator.num_pages)

    context = {
        'posts': filter_qs,
        'filterset': filterset,
        'page_obj': filter_qs,
        'paginator': paginator,
        #'cats': Category.objects.all(),
        #'current_time': timezone.localtime(timezone.now()),
        #'timezones': pytz.common_timezones
    }

    return render(request, 'news/search.html', context=context)

class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = string_news
        #author = Author.objects.get(user_id=self.request.user)  # берем автора новости, который зашел в систему
        news.author_id = 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = _('Создание новости:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

