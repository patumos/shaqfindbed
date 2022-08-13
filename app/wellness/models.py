from django.db import models

# Create your models here.

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

from django_quill.fields import QuillField
from django.conf import settings
import csv
import haversine as hs
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from shaqfindbed.utils import get_current_user
import decimal

from taggit.managers import TaggableManager

from multiselectfield import MultiSelectField

from django.utils.html import escape, format_html

DAY_CHOICES = (('sun', 'Sunday'),
              ('mon', 'Monday'),
              ('tue', 'Tuesday'),
              ('wed', 'Wednesday'),
              ('thu', 'Thursday'),
              ('fri', 'Friday'),
              ('sat', 'Saturday'),
               )

class GenericModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_created', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_modified', on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class StoreCatManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class StoreCat(GenericModel, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


    objects = StoreCatManager()

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return f"{self.name}"

    def natural_key(self):
        return self.name


class WellnessStore(GenericModel, models.Model):
    feature_image  = models.ImageField(upload_to="uploads/%Y/%m/%d/", blank=True,  null=True)
    name = models.CharField(max_length=200)
    body = QuillField()
    address_text = models.TextField(blank=True, null=True)
    #address = models.CharField(max_length=100)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)


    province = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    sha15_rating = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    tel = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=300, null=True, blank=True)
    line_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)



    store_cat = TreeForeignKey('StoreCat', on_delete=models.SET_NULL, null=True)

    #created_at = models.DateTimeField(auto_now_add=True, null=True)
    #updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    open_days = MultiSelectField(choices=DAY_CHOICES, null=True)
    open_time = models.TimeField(blank=False, null=True)
    close_time = models.TimeField(blank=False, null=True)
    status = models.CharField(
        max_length=30,
        choices=(("draft", "Draft"), ("publish", "Publish")),
        default="draft",
        null=True,
    )

    def image_tag(self):
        return format_html('<img src="%s" width="300px"/>' % escape(self.feature_image.url))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


    def __str__(self):
        return f"{self.name}"

    @property
    def store_cat_name(self):
        if self.store_cat:
            return self.store_cat.name
        else:
            return "-"



class StorePhoto(GenericModel, models.Model):
    name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    photo  = models.ImageField(upload_to="uploads/%Y/%m/%d/", blank=True, verbose_name="Photo")
    store = models.ForeignKey('WellnessStore', on_delete=models.CASCADE, null=True)

    def image_tag(self):
        return format_html('<img src="%s" width="300px"/>' % escape(self.photo.url))



class WellnessImportFile(models.Model):
    store_file  = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True, verbose_name="Store (csv)")

    def save(self, *args, **kwargs):
        super(WellnessImportFile, self).save(*args, **kwargs)

        with self.store_file.open('r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            WellnessStore.objects.all().delete()
            line_count = 0

            for r in csv_reader:
                if line_count > 0:
                    print(r)
                    print(f"{r[7]},{r[6]}, {r[17]}, {r[18]}")
                    try:
                        gp = map_fields.GeoPt(lat=float(r[17]), lon=float(r[18]))
                        print("gp error")
                        #location = fromstr(f'POINT({r[7]} {r[6]})', srid=4326)
                        #print(location)
                        '''
                        sc = StoreCat.objects.filter(name=r[6])
                        print(sc)
                        t = None
                        if len(sc) == 0:
                            t = StoreCat(name=r[6])
                            t.save()
                        else:
                            t = sc[0]
                        '''
                        '''
                        h = WellnessStore(name=r[1],body=r[2], province=r[5],  address_text=r[9], geolocation=gp, address=r[16], rating=r[8], store_cat=t, code=r[7], tel=r[10], website=r[11], email=r[12], line_id=r[13], sha15_rating=r[15])
                        h.save()
                        '''

                        h = WellnessStore(name=r[1],body='', province=r[5],  address_text=r[9], geolocation=gp, address=r[16], store_cat=None, code=r[7], tel=r[10], website=r[11], email=r[12], line_id=r[13])
                        h.save()
                        #return

                    except Exception as e:
                        print(e)

                line_count += 1



