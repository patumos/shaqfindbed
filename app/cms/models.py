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
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from shaqfindbed.utils import get_current_user
from django_quill.fields import QuillField

from django.utils.html import escape, format_html
from taggit.managers import TaggableManager
# Create your models here.


class GenericModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_created', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_modified', on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class PostCat(GenericModel, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return f"{self.name}"


class Post(GenericModel, models.Model):
    feature_image  = models.ImageField(upload_to="uploads/%Y/%m/%d/", blank=True,  null=True)
    title = models.CharField(max_length=200)
    body = QuillField()
    #body = models.TextField(blank=True, null=True)
    cat = models.ForeignKey('PostCat', on_delete=models.SET_NULL, null=True)
    tags = TaggableManager()
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
        return f"{self.title}"


class PostPhoto(GenericModel, models.Model):
    name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    photo  = models.ImageField(upload_to="uploads/%Y/%m/%d/", blank=True, verbose_name="Photo")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)

    def image_tag(self):
        return format_html('<img src="%s" width="300px"/>' % escape(self.photo.url))


