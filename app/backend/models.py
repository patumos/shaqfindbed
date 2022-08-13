#from django.db import models
from django.contrib.gis.db import models
from django_google_maps import fields as map_fields
from colorfield.fields import ColorField
#from smart_selects.db_fields import GroupedForeignKey
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

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
# Create your models here.
GENDER_CHOICES = (
    ('นางสาว','นางสาว'),
    ('นาย','นาย'),
    ('นาง', 'นาง'),
    ("ด.ช.","เด็กชาย"),
    ("ด.ญ.","เด็กหญิง"),
)

class Ambulance(models.Model):
    code = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    comment  = models.TextField(blank=True, null=True)

    color = ColorField(default='#FF0000')
    status = models.CharField(
        max_length=30,
        choices=(("working", "Working"), ("free", "Free"), ("ma", "MA")),
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.license_plate} ({self.get_status_display()}) {self.code} {self.brand} / {self.model_name}"

class Driver(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    idcard = models.CharField(max_length=20, null=True, blank=False)
    prefix = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
    )
    sex = models.CharField(
        max_length=30,
        choices=(("male", "Male"), ("female", "Female"),),
        null=True,
    )
    photo  = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True, verbose_name="Photo")

    address  = models.TextField(blank=True, null=True)
    #test
    status = models.CharField(
        max_length=30,
        choices=(("working", "Working"), ("free", "Free"), ("block", "Block")),
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_status_display()})"

class AmbulanceTicket(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True)

    status = models.CharField(
        max_length=30,
        choices=(("working", "Working"), ("free", "Free"), ("ma", "MA")),
        null=True,
    )

    checkin_at = models.DateTimeField(null=True, blank=True)
    checkout_at = models.DateTimeField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        super(AmbulanceTicket, self).save(*args, **kwargs)
        self.ambulance.status = self.status
        self.ambulance.save()
        self.driver.status = "working"
        self.driver.save()

    def __str__(self):
        return f"{self.driver}@{self.ambulance}"

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    age = models.IntegerField(null=True, blank=True)
    idcard = models.CharField(max_length=20, null=True, blank=False)
    tel = models.CharField(max_length=100, null=True, blank=True)
    line_id = models.CharField(max_length=100, null=True, blank=True)
    prefix = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
    )
    sex = models.CharField(
        max_length=30,
        choices=(("male", "Male"), ("female", "Female"),),
        null=True,
    )
    photo  = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True, verbose_name="Photo")

    address = map_fields.AddressField(max_length=200, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, null=True)
    condition_level = models.CharField(
        max_length=30,
        choices=(("green", "Green"), ("yellow", "Yellow"), ("red", "Red")),
        null=True,
    )
    comment  = models.TextField(blank=True, null=True)
    address_text  = models.TextField(blank=True, null=True)
    #test
    patient_status = models.CharField(
        max_length=30,
        choices=(("request", "Request"), ("process", "Process"), ("complete", "Complete")),
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        #self.nearby()
        return f"{self.first_name} {self.last_name}"



    def nearby_from_db(self, dlimit):
        bd = ""
        temps = []
        try:
            for h0 in  Hospital.objects.all():
                p2 = (h0.geolocation.lat, h0.geolocation.lon)
                p1 = (self.geolocation.lat, self.geolocation.lon)
                d = round(hs.haversine(p1,p2), 2)
                if d < dlimit:
                    #bd += f"<tr><td>{h0.title}</td><td>{d}km</td></tr>"
                    temps.append({'title': h0.title, 'd': d, 'id': h0.id, 'beds': h0.free_beds()})
                    #print(f"to {h0.title} => {hs.haversine(p1, p2)}km")

            temps.sort(key= lambda s: s['d'], reverse=False)
            for t in temps:
                bd += f"<tr><td><a href='/admin/backend/hospital/{t['id']}/change/' target='_blank'>{t['title']}</a></td><td>{t['d']} km</td><td>{t['beds']}</td></tr>"

            rt = f'''
    <br>
            <table><thead><tr><th>Hospital</th><th>Distance</th><th>Free Beds</th></tr></thead>
            <tbody>
                {bd}
            </tbody>
            </table>
            '''
            return rt
        except:
            return "-"

    def nearby(self):
        #self.nearby_from_db()
        try:
            r = gmaps.places_nearby(location=(self.geolocation.lat, self.geolocation.lon), type="hospital", radius=10000)
            bd = ""
            for r0 in r['results']:
                openh = "-"
                if 'opening_hours' in r0:
                    openh = r0['opening_hours']['open_now']
                else:
                    openh = "-"

                bd += f"<tr><td>{r0['name']}</td><td>{openh}</td><td>{r0['vicinity']}</td></tr>"

            rt = f'''
    <br>
            <table><thead><tr><th>Name</th><th>Opening Hours</th><th>Vicinity</th></tr></thead>
            <tbody>
                {bd}
            </tbody>
            </table>
            '''
            return rt
        except:
            return "-"



class ImportFile(models.Model):
    hospital_file  = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True, verbose_name="Hospital (csv)")

    def save(self, *args, **kwargs):
        super(ImportFile, self).save(*args, **kwargs)

        with self.hospital_file.open('r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            Hospital.objects.all().delete()
            line_count = 0

            for r in csv_reader:
                if line_count > 0:
                    print(r)
                    print(f"{r[7]},{r[6]}")
                    try:
                        gp = map_fields.GeoPt(lat=float(r[6]), lon=float(r[7]))

                        location = fromstr(f'POINT({r[7]} {r[6]})', srid=4326)
                        print(location)
                        h = Hospital(title=r[3], address_text=r[5], geolocation=gp, address=r[3])
                        h.save()
                    except Exception as e:
                        print(e)

                line_count += 1



class Place(models.Model):
    #title  = models.Char
    title = models.CharField(max_length=200, blank=True, null=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    more_info  = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.address} ({self.geolocation})"




class Hospital(models.Model):
    title = models.CharField(max_length=200)
    location = models.PointField(blank=True, null=True)
    address_text = models.TextField(blank=True, null=True)
    #address = models.CharField(max_length=100)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    tel = models.CharField(max_length=100, null=True, blank=True)
    line_id = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.address_text}"

    def free_beds(self):
        return self.bed_set.filter(~Q(occupy=True)).count()


class Points(models.Model):
    #src  = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=False, related_name='src')
    #ticket = models.ForeignKey(AmbulanceTicket, on_delete=models.SET_NULL, null=True)
    dest  = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=False)
    address = map_fields.AddressField(max_length=200, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, null=True)

    distance = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=7, verbose_name="Distance (km)")
    duration = models.CharField(max_length=200, null=True, blank=True)

    directions  = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
        print(geocode_result)
        print(self.geolocation)
        origin = [(self.geolocation.lat, self.geolocation.lon)]
        dest = [(self.dest.geolocation.lat, self.dest.geolocation.lon)]
        dst = gmaps.distance_matrix(origin, dest)
        dirs = gmaps.directions(origin[0], dest[0])
        self.directions = dirs
        print(dirs)
        self.distance = dst['rows'][0]['elements'][0]['distance']['value'] / 1000
        self.duration = dst['rows'][0]['elements'][0]['duration']['text']
        print(dst)
        super(Points, self).save(*args, **kwargs)

class Bed(models.Model):
    code = models.CharField(max_length=30)
    occupy = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.code


class PatientLog(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    bed = ChainedForeignKey(
        "Bed",
        chained_field="hospital",
        chained_model_field="hospital",
        show_all=False,
        auto_choose=True,
        null=True
    )
    notes  = models.TextField(blank=True, null=True)
    condition_level = models.CharField(
        max_length=30,
        choices=(("green", "Green"), ("yellow", "Yellow"), ("red", "Red")),
        null=True,
    )
    status = models.CharField(
        max_length=30,
        choices=(("active", "Active"), ("inactive", "Inactive"), ("transfer", "Transfer")),
        null=True,
    )
    checkin_at = models.DateTimeField(null=True, blank=True)
    checkout_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)




