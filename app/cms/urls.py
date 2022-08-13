from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<post_id>', views.post, name='view_post'),
    path('tags/<tag>', views.post_tags, name='tags'),
]
