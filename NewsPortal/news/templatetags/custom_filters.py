from django import template
import re # работа с регулярными выражениями

from django.template.defaultfilters import stringfilter

register = template.Library()

bad_words = ['очень', 'плохие', 'слова', 'что', 'для']

fuck_words = ['заеб', 'охуенный', 'охуенно', 'сука', 'бля', 'блять', 'курва', 'хуй', 'пиздец', 'пизд', 'ебнутый', 'ёбнутый', 'ебанутый', 'fuck', 'damn', 'bitch', 'douchebag', 'asshole', 'poop']


def replace(match):
    word = match.group()
    if word.lower() in fuck_words:
        return word[0] + '*' * (len(word) - 1)
    else:
        return word


# Регистрируем наш фильтр censor - цензор слов, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
@stringfilter
def censor(value):
# value: значение, к которому нужно применить фильтр

   # Возвращаемое функцией значение подставится в шаблон.
   return re.sub(r'\b\w*\b', replace, value, flags=re.I | re.U)

@register.filter
def hash(h, key):
    s=h[key]
    return ','.join(i[0] for i in s)

