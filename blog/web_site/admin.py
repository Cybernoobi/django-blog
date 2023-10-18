from django.contrib import admin

from .models import Category, Article


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'view', 'category', 'author')
    list_display_links = ('pk', 'title')
    list_filter = ('created_at', 'category', 'author')
    list_editable = ('category', 'author')
    readonly_fields = ('view',)


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
