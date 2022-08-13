from django.db import models

from django_google_maps import fields as map_fields
from colorfield.fields import ColorField
from smart_selects.db_fields import (
    ChainedForeignKey,
    ChainedManyToManyField,
    GroupedForeignKey,
)
from django.db.models import Q
import googlemaps
from django.contrib.gis.geos import fromstr

from django.conf import settings
import csv
import haversine as hs
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from shaqfindbed.utils import get_current_user
import decimal
# Create your models here.

VAT = 0.07

class GenericModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_created', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_modified', on_delete=models.SET_NULL)

    '''
    def save(self, *args, **kwargs):
        user = get_current_user()
        print("user "+user.is_authenticated())
        if user and user.is_authenticated():
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(GenericModel, self).save(*args, **kwargs)
    '''

    class Meta:
        abstract = True

class StoreCat(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return f"{self.name}"

class Store(GenericModel, models.Model):
    name = models.CharField(max_length=200)
    address_text = models.TextField(blank=True, null=True)
    #address = models.CharField(max_length=100)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)


    tel = models.CharField(max_length=100, null=True, blank=True)
    line_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    store_cat = TreeForeignKey('StoreCat', on_delete=models.SET_NULL, null=True)

    #created_at = models.DateTimeField(auto_now_add=True, null=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"



class ProductType(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return f"{self.name}"


class Buyer(GenericModel, models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    address_text = models.TextField(blank=False, null=False)

    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)


    tel = models.CharField(max_length=100, null=False, blank=False)
    line_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


    def __str__(self):
        return f"{self.name} Tel.:{self.tel} Email:{self.email}"

class Inbox(GenericModel, models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=False)
    buyer = models.ForeignKey('Buyer', on_delete=models.SET_NULL, null=True, blank=True)

    subject = models.CharField(max_length=200)
    body = models.TextField(blank=False)

    tel = models.CharField(max_length=100, null=True, blank=True)
    line_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


    status = models.CharField(
        max_length=30,
        choices=(("request", "Request"), ("read", "Read"), ("process", "Process"), ("complete", "Complete")),
        default="request",
    )

class Purchase(GenericModel, models.Model):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, null=False, blank=False)
    store = models.ForeignKey('Store', on_delete=models.DO_NOTHING, null=False, blank=False)
    vendor = models.ForeignKey('Vendor', on_delete=models.DO_NOTHING, null=False, blank=False)

    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)
    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)


    sub_total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    vat = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    def save(self, *args, **kwargs):
        self.sub_total = self.price * self.n_unit
        self.vat  = self.sub_total * decimal.Decimal(VAT)
        self.total = self.sub_total + self.vat
        super(Purchase, self).save(*args, **kwargs)

class Sale(GenericModel, models.Model):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, null=False, blank=False)
    store = models.ForeignKey('Store', on_delete=models.DO_NOTHING, null=False, blank=False)
    sku = models.ForeignKey('ProductSKU', on_delete=models.DO_NOTHING, null=False, blank=False)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)
    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)
    buyer = models.ForeignKey('Buyer', on_delete=models.DO_NOTHING, null=False, blank=False)


    sub_total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    vat = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)

    def save(self, *args, **kwargs):
        self.sub_total = self.price * self.n_unit
        self.vat  = self.sub_total * decimal.Decimal(VAT)
        self.total = self.sub_total + self.vat
        super(Sale, self).save(*args, **kwargs)

class Product(GenericModel, models.Model ):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    product_type = TreeForeignKey('ProductType', on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)


    details  = models.JSONField(null=True, blank=True)

    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name} {self.code}"


class VendorProduct(GenericModel, models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)
    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.product.name} {self.price}/{self.unit_name}"

class Vendor(GenericModel, models.Model ):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    #product_type = TreeForeignKey('ProductType', on_delete=models.SET_NULL, null=True)
    #product = models.ForeignKey('Product', on_delete=models.CASCADE)
    #products = models.ManyToManyField('Product',)
    description = models.TextField(blank=True, null=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=True, blank=False)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)


    details  = models.JSONField(null=True, blank=True)

    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)

    tel = models.CharField(max_length=100, null=True, blank=True)
    line_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    address_text = models.TextField(blank=False, null=False)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)


    def __str__(self):
        return f"{self.name} {self.code}"


class VendorOrder(GenericModel, models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE,  null=False, blank=False)
    product = ChainedForeignKey(
        "VendorProduct",
        chained_field="vendor",
        chained_model_field="vendor",
        show_all=False,
        auto_choose=True,
        null=True
    )
    store = models.ForeignKey('Store', on_delete=models.CASCADE, null=False, blank=False)

    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)

    sub_total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    vat = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)


    def save(self, *args, **kwargs):
        self.sub_total = self.price * self.n_unit
        self.vat  = self.sub_total * decimal.Decimal(VAT)
        self.total = self.sub_total + self.vat
        super(VendorOrder, self).save(*args, **kwargs)

class ProductSKU(GenericModel, models.Model ):
    sku = models.CharField(max_length=200)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7)

    details  = models.JSONField(null=True, blank=True)

    n_unit = models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)
    unit_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.sku} {self.product} @{self.price}(THB)"

class Photo(GenericModel, models.Model):
    name = models.CharField(max_length=200,  blank=True)
    order_n = models.IntegerField(default=0, blank=True)
    photo  = models.ImageField(upload_to="uploads/%Y/%m/%d/", blank=False, verbose_name="Photo")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    roles = models.CharField(
        max_length=30,
        choices=(("seller", "Seller"), ("buyer", "Buyer"),),
        default="seller",
    )
    tel = models.CharField(max_length=100, null=True, blank=False)
    line_id = models.CharField(max_length=100, null=True, blank=False)
    facebook = models.CharField(max_length=200, null=True, blank=False)

    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        store = Store()
        store.name = "Unname"
        store.created_by = instance
        store.save()
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        Profile.objects.create(user=instance)
