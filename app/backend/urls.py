from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('import_file', views.import_file, name='import_file'),
     url(
        r'^hospital-autocomplete/$',
        views.HospitalAutocomplete.as_view(),
        name='hospital-autocomplete',
    ),
]
