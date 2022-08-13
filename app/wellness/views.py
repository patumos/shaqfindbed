from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import WellnessStore
from django.core import serializers
import json
import haversine as hs
from django.db.models import Q
# Create your views here.
def api_stores(request):
    stores = WellnessStore.objects.all()
    #store_list = serializers.serialize('json', stores)
    #rs  = json.dumps(store_list)
    #print(rs)
    data = serializers.serialize("json", stores, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type="application/json")
    #return JsonResponse({'stores': store_list}, safe=False)

def api_store_id(request, pk):
    stores = WellnessStore.objects.get(pk = pk)
    #store_list = serializers.serialize('json', stores)
    #rs  = json.dumps(store_list)
    #print(rs)
    data = serializers.serialize("json", [stores], use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type="application/json")
    #return JsonResponse({'stores': store_list}, safe=False)

def api_store_photos_id(request, pk):
    stores = WellnessStore.objects.get(pk = pk)
    #store_list = serializers.serialize('json', stores)
    #rs  = json.dumps(store_list)
    #print(rs)
    data = serializers.serialize("json", stores.storephoto_set.all(), use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type="application/json")
    #return JsonResponse({'stores': store_list}, safe=False)

def api_nearme(request):
    dlimit = 100
    bd = ""
    temps = []
    loc  = request.GET.get('location', None)

    lat = float(loc.split(',')[0])
    lng = float(loc.split(',')[1])
    ids = []
    dist = []
    try:
        for h0 in  WellnessStore.objects.all():
            p2 = (h0.geolocation.lat, h0.geolocation.lon)
            p1 = (lat, lng)
            d = round(hs.haversine(p1,p2), 2)
            if d < dlimit:
                #dist.append(d)
                ids.append({'d': d, 'id': h0.id})

    except:
        print("Error")

    ids = sorted(ids, key=lambda k: k['d'])

    temp_id = [d['id'] for d in ids]

    stores = WellnessStore.objects.filter(id__in  = temp_id)
    data = serializers.serialize("json", stores, use_natural_foreign_keys=True, use_natural_primary_keys=True)

    return HttpResponse(data, content_type="application/json")



def api_search(request):
    q = request.GET.get('q', None)
    if q:
        stores = WellnessStore.objects.filter(Q(name__contains=q) | Q(body__contains=q))
        #store_list = serializers.serialize('json', stores)
        #rs  = json.dumps(store_list)
        #print(rs)
        data = serializers.serialize("json", stores, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse({'error': True}, content_type="application/json")
