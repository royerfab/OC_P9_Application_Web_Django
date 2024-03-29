from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username


@register.filter
def model_type(value):
    return type(value).__name__
