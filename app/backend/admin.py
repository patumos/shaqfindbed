from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Hospital, Patient, Bed, PatientLog, Driver, Ambulance, AmbulanceTicket, Place, Points, ImportFile
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from django.utils.html import format_html
from django.conf import settings

from dal import autocomplete
from django import forms


class PointForm(forms.ModelForm):
    class Meta:
        model = Points
        fields = ('__all__')
        widgets = {
            'dest': autocomplete.ModelSelect2(url='hospital-autocomplete'),
            'address': map_widgets.GoogleMapsAddressWidget,
            'directions': JSONEditorWidget,
        }

#@admin.register(Bed)

@admin.register(ImportFile)
class ImportFileAdmin(admin.ModelAdmin):
    pass

class PointInlineAdmin(admin.StackedInline):
    model = Points
    form = PointForm
    #readonly_fields = ('distance', 'duration', 'get_map')
    #fields = ('hospital', 'notes', 'condition_level', 'status')

@admin.register(AmbulanceTicket)
class AmbulanceTicketAdmin(admin.ModelAdmin):
    #inlines = [PointInlineAdmin,]
    list_display = ('driver', 'ambulance', 'checkin_at', 'checkout_at', 'status')


@admin.register(Points)
class PointAdmin(admin.ModelAdmin):
    form = PointForm
    readonly_fields = ('distance', 'duration', 'get_map')

    '''
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
        models.JSONField: {'widget': JSONEditorWidget},
    }
    '''

    def get_map(self, obj):
         return format_html( f'''
<br>
<div>
<iframe
  width="100%"
  height="450"
  style="border:0"
  loading="lazy"
  allowfullscreen
  src="https://www.google.com/maps/embed/v1/directions?key={settings.GOOGLE_MAPS_API_KEY}&origin={obj.geolocation.lat},{obj.geolocation.lon}&destination={obj.dest.geolocation.lat},{obj.dest.geolocation.lon}"></iframe></div>''')

    fields = ('dest', 'address', 'geolocation', 'distance', 'duration', 'directions','get_map' )
    #pass

#@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
        models.JSONField: {'widget': JSONEditorWidget},
    }
    #pass
    #list_display = ('driver', 'ambulance', 'checkin_at', 'checkout_at', 'status')

@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'license_plate', 'brand', 'status')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

class BedAdmin(admin.TabularInline):
    model = Bed


class PatientLogForm(forms.ModelForm):
    class Meta:
        fields = ('__all__')

        widgets = {
            'hospital': autocomplete.ModelSelect2(url='hospital-autocomplete'),
        }

class PatientLogAdmin(admin.StackedInline):
    model = PatientLog
    form = PatientLogForm
    #fields = ('hospital', 'notes', 'condition_level', 'status')


@admin.register(Hospital)
class HospitalAdmin(OSMGeoAdmin):
    search_fields = ('title',)
    list_display = ('title', 'address', 'geolocation')
    inlines = [BedAdmin,]
    fields = ('title', 'address_text', 'tel', 'line_id', 'address', 'geolocation',)
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ('first_name','last_name', 'idcard',  'address', 'patient_status')
    list_display = ('first_name','last_name', 'idcard',  'address', 'patient_status', 'created_at')
    readonly_fields = ('nearby_from_db', 'nearby_places',  )
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
    inlines = [PatientLogAdmin,]

    def nearby_places(self, obj):
        r = obj.nearby()
        return format_html(r)

    def nearby_from_db(self, obj):
        r = obj.nearby_from_db(20)
        return format_html(r)
