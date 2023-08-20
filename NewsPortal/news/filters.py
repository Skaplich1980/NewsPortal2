import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import *

class NewsFilter(FilterSet):
    row_date = django_filters.DateFilter(field_name='date_create', lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # поиск по тексту
            'text': ['icontains'],
            # поиск по типу
            #'categoryType': ['exact'],
        }
        labels = {
            'title': 'Заголовок публикации',
            'text': 'Текст публикации',
            #'types': 'Тип',
        }