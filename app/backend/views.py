from django.shortcuts import render
from dal import autocomplete

from .models import Hospital
# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'backend/index.html')

def import_file(request):
    return render(request, 'backend/import_file.html')



class HospitalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Hospital.objects.none()

        qs = Hospital.objects.all()

        if self.q:
            qs = qs.filter(title__contains=self.q)

        return qs
