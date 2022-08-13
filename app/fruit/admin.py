from django.contrib import admin

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Store, ProductType, Product, Photo, ProductSKU, StoreCat, Buyer, Sale, Inbox, Vendor, VendorOrder
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
from mptt.admin import TreeRelatedFieldListFilter
from shaqfindbed.utils import UtilModel




@admin.register(Store)
class StoreAdmin(UtilModel, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'address', 'geolocation', 'created_at', 'created_by')
    fields = ('name', 'store_cat', 'address_text',  'tel', 'line_id',  'email', 'address', 'geolocation',)
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

@admin.register(Vendor)
class VendorAdmin(UtilModel, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'code', 'created_at', 'created_by')
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

@admin.register(VendorOrder)
class VendorOrderAdmin(UtilModel, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('vendor', 'product', 'store', 'price',  'n_unit',  'unit_name', 'created_at', 'created_by')
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

@admin.register(Buyer)
class BuyerAdmin(UtilModel, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'tel', 'address_text', 'geolocation', 'created_at', 'created_by')
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }



@admin.register(ProductType)
class ProductTypeAdmin(MPTTModelAdmin):
    pass


@admin.register(StoreCat)
class StoreCatAdmin(MPTTModelAdmin):
    pass



class PhotoInlineAdmin(admin.StackedInline):
    model = Photo

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInlineAdmin,]

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
        models.JSONField: {'widget': JSONEditorWidget},
    }
    list_display = ["name", "created_at", "created_by"]

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        #super().save_model(request, obj, form, change)
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProductSKU)
class ProductSKUAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
        models.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    list_display = ["store", "product",  "buyer",  "subject", "created_by"]

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ("product", "store", "sku", "price", "n_unit", "unit_name",  "buyer", 'sub_total', 'vat', 'total' )
    readonly_fields = ('sub_total', 'vat', 'total',)



