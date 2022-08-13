
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('api/stores', views.api_stores, name='api_stores'),
    path('api/stores/<pk>', views.api_store_id, name='api_store_id'),
    path('api/search', views.api_search, name='api_search'),
    path('api/stores/<pk>/photos', views.api_store_photos_id, name='api_store_photos_id'),
    path('api/nearme', views.api_nearme, name='api_nearme'),

]

app_name = 'wellness'
