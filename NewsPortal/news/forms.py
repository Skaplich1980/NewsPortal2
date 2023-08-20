from django import forms
from .models import Post
class PostForm(forms.ModelForm):

# вывод, для проверки
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
       model = Post
       fields = [
          # 'author', автоматически
           'title',
          # 'date_create',автоматически
           'postCategory',
           'text'
       ]
       labels = {
           'title':'Заголовок',
           'postCategory':'Категория',
           'text':'текст публикации',
       }