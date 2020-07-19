from django.shortcuts import render
from pricing.models import Station


# Create your views here.

def index(request):
    stations = [str(station) for station in Station.objects.all()]
    station_str = '[\"%s\"]'%'\",\"'.join(stations)
    print(station_str)
    context = {'stations': station_str}
    return render(request, "index.html", context)
