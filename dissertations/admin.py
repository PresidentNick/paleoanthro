from django.contrib import admin
from models import Dissertation


class DissertationAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'author_last_name', 'title',)
    list_display_links = ['id']
    list_filter = ['year']
    search_fields = ['id', 'author_last_name', 'author_first_name', 'title', 'publisher']


admin.site.register(Dissertation, DissertationAdmin)
