from django import template

register = template.Library()
censored_words = [
    'редиска', 'Редиска'
]


@register.filter()
def censor(text):
    if isinstance(text, str):
        censored_text = text
        for censored_word in censored_words:
            censored_text = text.replace(censored_word, '*' * len(censored_word))
        return censored_text
    else:
        return text

