from django import template

from web_site.models import Category, Favorite


register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def is_article_added_to_fav_to_user(user, article):
    obj = Favorite.objects.filter(user=user, article=article).first()
    if obj is not None:
        return True
    return False
    