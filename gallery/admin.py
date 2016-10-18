from django.contrib import admin
from gallery.models import *
from loginer.models import User


class PictureInline(admin.StackedInline):
    model = Comment
    extra = 0


class PictureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['id_user','name_of_picture']}),

    ]

    inlines = [PictureInline]
    list_filter = ['date_of_add']
    search_fields = ['id_user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ( 'comments', 'id_user','id_picture')
    fieldsets = [
        (None, {'fields': ['comments']}),
        ('User nickname', {'fields': ['id_user']}),

    ]
    list_filter = ['id_picture','id_user']


admin.site.register(Picture, PictureAdmin)
admin.site.register(Comment, CommentAdmin)
