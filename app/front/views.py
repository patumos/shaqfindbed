from django.shortcuts import render, redirect
from backend.models import Patient
from wellness.models import WellnessStore

# Create your views here.

def index(request):
    stores = WellnessStore.objects.all()
    '''
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        p = Patient()
        p.first_name = request.POST.get('firstName')
        p.last_name = request.POST.get('lastName')
        #p.idcard = request.POST.get('idCard')
        p.address = request.POST.get('address')
        p.geolocation = request.POST.get('geo')
        p.birth_date = request.POST.get('bd')
        p.comment = request.POST.get('comment')
        p.tel = request.POST.get('tel')
        p.line_id = request.POST.get('line_id')
        p.photo = request.FILES.get('photo')
        p.patient_status = "request"
        p.save()
        return redirect('success')
    '''
    return render(request, 'front/index.html', {'stores': stores})

def news(request):
    pass

def forum(request):
    pass

def articles(request):
    pass

def fruit_market(request):
    pass

def agri_market(request):
    pass



def mystore(requeset):
    pass


def success(request):
    return render(request, 'front/success.html')

def tracking(request):
    return render(request, 'front/tracking.html')

def my404(request,exception):
    return render(request, 'front/404.html')
    #return redirect("index")

# def province(request):
#     return render(request, 'front/province.html')

def province(request, proname):
    stores = WellnessStore.objects.filter(province=proname)
    return render(request, 'front/province.html', {'proname': proname, 'stores': stores})

def place(request, catname):
    if catname == "นวดไทย":
        catname = "นวดไทย/สปา"
    stores = WellnessStore.objects.filter(store_cat__name=catname)
    return render(request, 'front/place.html', {'stores': stores, 'catname': catname})

# def place(request, catn):
#     place = WellnessStore.objects.get(store_cat=catn)
#     return render(request, 'front/place.html',{'place': place})

def placedetail(request, oid):
    store = WellnessStore.objects.get(pk=oid)
    return render(request, 'front/placedetail.html',{'store': store})
