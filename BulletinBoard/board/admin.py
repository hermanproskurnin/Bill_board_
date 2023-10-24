from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Advertisement, Category, Comment, Mailing


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'like', 'dislike', 'date_time', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.media_file:
            return mark_safe(f'<img src={obj.media_file.url} width="50" height="60">')
        else:
            return

    get_image.short_description = 'Изображение'


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Mailing)
