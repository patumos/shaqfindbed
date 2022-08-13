
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('province', views.province),
    path('province/<proname>', views.province, name='store_province'),
    path('place/<catname>', views.place, name='store_cat'),
    # path('place/<catn>', views.place, name='place'),
    path('placedetail/<oid>', views.placedetail, name='placedetail'),
    path('tracking', views.tracking, name='tracking'),
    path('tracking', views.tracking, name='tracking'),
    path('success', views.success, name='success'),
]

app_name = 'front'
