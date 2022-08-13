from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Post, PostCat, PostPhoto
# Register your models here.

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from django.utils.html import format_html
from django.conf import settings

from dal import autocomplete
from django import forms
from mptt.admin import MPTTModelAdmin
# Register your models here.

class UtilModel:
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        #super().save_model(request, obj, form, change)
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class PostPhotoInlineAdmin(admin.StackedInline):
    model = PostPhoto
    readonly_fields = ('image_tag',)

@admin.register(Post)
class PostAdmin(UtilModel, admin.ModelAdmin):
    list_display = ('title', 'created_at', 'created_by')
    fields = ("feature_image", "image_tag", "title", "body", "cat",  "tags", "status")
    readonly_fields = ('image_tag',)

    inlines = [PostPhotoInlineAdmin,]

@admin.register(PostCat)
class PostCatAdmin(UtilModel, admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by')
    #pass
