from django.contrib import admin
from models import Content, Review


class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'article_type', 'year',)
    list_display_links = ['id', 'title']
    list_filter = ['year', 'article_type']
    search_fields = ['id', 'title', 'authors', 'abstract_text', 'year']
    exclude = ('article',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'book_authors', 'year', 'reviewer', 'status',)
    list_display_links = ['id', 'title']
    list_filter = ['year', 'reviewer', 'status']
    search_fields = ['id', 'title', 'book_authors', 'year', 'reviewer', 'review_title']

admin.site.register(Content, ContentAdmin)
admin.site.register(Review, ReviewAdmin)