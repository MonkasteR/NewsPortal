from django import template

register = template.Library()
# Список цензурируемых слов. По идее создать модель для этого и туда накидать или внешним файлом подключить. Но лень.
censor_words = ['чебурашка', 'дурак', 'лама']


@register.filter()
def censorship(value):
    words = value.split()  # Разделяем текст на слова
    censored_words = []

    for word in words:
        # Если слово находится в списке для цензуры, заменяем его на звездочки по количеству букв в слове
        if word.lower() in censor_words:  # для проверки приводим к нижнему регистру
            censored_words.append('*' * len(word))
        else:
            censored_words.append(word)

    return ' '.join(censored_words)  # Собираем обратно в текст
