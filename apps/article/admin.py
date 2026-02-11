from django.contrib import admin

from apps.article.models import Article, Comment

admin.site.register(Comment)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_at"]
