from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
import pytz
from django.utils.translation import gettext as _
from django.utils import timezone
from .models import Post, POST_TYPES, news as string_news, article as string_article
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string
#from django.core.cache import cache
#from .tasks import *
#from django.views.decorators.cache import cache_page
#from django.utils.translation import gettext as _

from django.core.management.utils import get_random_secret_key


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
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        context['cats'] = Category.objects.all()
        print(context['cats'])

        t_list = {} # получение списка категорий новостей
        for q in self.filterset.qs:
            t_list[q.id] = list(q.categories.values_list('name'))
        context['fcats'] = t_list

        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['username'] = self.request.user.username
        context['pcats'] = Post.objects.select_related('PostCategory')
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельномой новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'news/post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = dict(POST_TYPES)[self.object.categoryType]
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['cats'] = Category.objects.all()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    # def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
    #     obj = cache.get(f'product-{self.kwargs["pk"]}',
    #                     None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
    #     # если объекта нет в кэше, то получаем его и записываем в кэш
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'product-{self.kwargs["pk"]}', obj)
    #     return obj


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

    t_list = {}  # получение списка категорий новостей
    for q in filterset.qs:
        t_list[q.id] = list(q.categories.values_list('name'))

    context = {
        'posts': filter_qs,
        'filterset': filterset,
        'page_obj': filter_qs,
        'paginator': paginator,
        'cats': Category.objects.all(),
        'fcats': t_list,
        'current_time': timezone.localtime(timezone.now()),
        'timezones': pytz.common_timezones
    }

    return render(request, 'news/search.html', context=context)

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = string_news
        author1 = Author.objects.get(Author_User=self.request.user)  # берем автора новости, который зашел в систему
        news.author = author1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = _('Создание новости:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context



class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = _('Редактирование новости:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        art = form.save(commit=False)
        art.categoryType = string_article
        author1 = Author.objects.get(Author_User=self.request.user)  # берем автора новости, который зашел в систему
        news.author = author1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = _('Создание статьи:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')

class UserDataUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserDataForm
    model = User
    template_name = 'account/user_edit.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Редактирование данных пользователя:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def get_object(self):
        return self.request.user


def logout_user(request):
    logout(request)
    return redirect('login')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('post_list')
    template_name = 'account/user_edit.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('post_list')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    Author.objects.create(Author_User=user)
    return redirect('post_list')

@login_required
def subscribe_on_cat(request, cat_id):
    user = request.user
    cat = Category.objects.get(id=cat_id)
    cat.subscribers.add(user)
    return redirect('category', cat_id=cat_id)

@login_required
def unsubscribe_cat(request, cat_id):
    user = request.user
    cat = Category.objects.get(id=cat_id)
    cat.subscribers.remove(user)
    return redirect('category', cat_id=cat_id)

def show_category(request, cat_id):
    posts = Post.objects.filter(categories__id=cat_id).order_by('-date_create')
    cats = Category.objects.all()
    try:
        already_subscribed = SubscribersCategory.objects.get(user_id=request.user.pk, category_id=cat_id)
    except SubscribersCategory.DoesNotExist:
        already_subscribed = None

    queryset = Post.objects.all()
    filterset = NewsFilter(request.GET, queryset)
    t_list = {}  # получение списка категорий новостей

    for q in filterset.qs:
        t_list[q.id] = list(q.categories.values_list('name'))
    context = {
        'posts': posts,
        'cats': cats,
        'fcats': t_list,
        'current_cat': Category.objects.get(id=cat_id),
        'already_subscribed': already_subscribed,
    }
    print(get_random_secret_key())
    return render(request, 'news/posts.html', context=context)

#def news_limit(request):
#    return render(request, 'news/post_limit.html')

