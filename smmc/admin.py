from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from .models import Tag, Entry


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'entries_count')
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(Count('entry'))

    def entries_count(self, obj):
        return obj.entry__count

    entries_count.admin_order_field = 'entry__count'
    entries_count.short_description = _('number of entries')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('id', 'active')
        }),
        (_('Date'), {
            'fields': ('year', 'month', 'day'),
            'description': _('This is the date of the event. If any of the following is unknown, leave it empty.')
        }),
        (_('Title and description'), {
            'fields': ('title', 'description')
        }),
        (_('Tags'), {
            'fields': ('tags', 'sort')
        }),
        (_('File'), {
            'fields': ('file', 'mime_type', 'md5sum')
        })
    )
    filter_horizontal = ['tags']
    list_display = ('id', 'year', 'month', 'day', 'title', 'sort', 'mime_type', 'tags_count')
    list_display_links = ['id']
    list_filter = ('mime_type', )
    readonly_fields = ['id', 'mime_type', 'md5sum']
    search_fields = ['id', 'date', 'title', 'description', 'tags__name']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(Count('tags'))

    def tags_count(self, obj):
        return obj.tags__count

    tags_count.admin_order_field = 'tags__count'
    tags_count.short_description = _('number of tags')
