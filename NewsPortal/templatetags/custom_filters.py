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


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name="is_subscribed")
def is_subscribed(category, user):
    return category.subscribers.filter(pk=user.pk).exists()
