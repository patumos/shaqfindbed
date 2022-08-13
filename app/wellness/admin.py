from django.contrib import admin

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import WellnessStore, StoreCat, StorePhoto, WellnessImportFile

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from django.utils.html import format_html
from django.conf import settings


from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter

from dal import autocomplete
from django import forms
# Register your models here.


from shaqfindbed.utils import UtilModel


@admin.register(StoreCat)
class StoreCatAdmin(MPTTModelAdmin):
    pass

class StorePhotoInlineAdmin(admin.StackedInline):
    model = StorePhoto
    readonly_fields = ('image_tag',)

@admin.register(WellnessImportFile)
class WellnessImportFileAdmin(admin.ModelAdmin):
    pass

@admin.register(WellnessStore)
class WellnessStoreAdmin(UtilModel, admin.ModelAdmin):
    list_display = ('name', 'province', 'created_at', 'created_by')
    fields = ("feature_image", "image_tag", "name", "body", "address", "geolocation", "address_text",  "province",
              "code",  "rating",  "tel",  "line_id",  "email",  "open_days", "open_time",  "close_time", "store_cat","tags", "status")
    readonly_fields = ('image_tag',)

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
        models.JSONField: {'widget': JSONEditorWidget},
    }
    inlines = [StorePhotoInlineAdmin,]




