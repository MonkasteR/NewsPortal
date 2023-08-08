from django import template

register = template.Library()

censor_words = ['чебурашка', 'дурак', 'лама']  # список цензурируемых слов.


@register.filter()
def censorship(value):
    words = value.split()  # Разделяем текст на слова
    censored_words = []

    for word in words:
        # Если слово находится в списке для цензуры, заменяем его на звездочки
        if word.lower() in censor_words:
            censored_words.append('*' * len(word))
        else:
            censored_words.append(word)

    return ' '.join(censored_words)  # Собираем обратно в текст
