import django_filters
from django.forms import DateInput
from django_filters import FilterSet, filters
from .models import *

class NewsFilter(FilterSet):
    row_date = django_filters.DateFilter(
        field_name='date_create',
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата'
    )
    title = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    text = django_filters.CharFilter(lookup_expr='icontains', label='Текст публикации')

    class Meta:
        model = Post
        fields = ['title', 'text']
