from django.shortcuts import render
from pricing.models import Station
from datetime import datetime
from .forms import TripForm
import pricing.data as d
import requests
import pricing.subscriptions as sub
import sys

if sys.version_info.minor < 6:
    raise SystemError("Need at least Python 3.6, found %s"%sys.version)
# Create your views here.

def index(request):
    stations = [str(station) for station in Station.objects.all()]
    station_str = '[\"%s\"]' % '\",\"'.join(stations)
    context = {'stations': station_str}
    if request.method == 'POST':
        form = TripForm(request.POST)
        context['form'] = form
        if form.is_valid():
            get_trip(form)
            return render(request, 'index.html', context)  # add trip data
    else:
        form = TripForm()
        context['form'] = form
    return render(request, "index.html", context)


def get_trip(form):
    dep_code = Station.objects.get(short=form.cleaned_data['departure']).code
    arr_code = Station.objects.get(short=form.cleaned_data['arrival']).code
    dep_datetime = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
    url = 'https://gateway.apiportal.ns.nl/public-prijsinformatie/prices'
    params = {'fromStation': dep_code, 'toStation': arr_code, 'plannedFromTime': dep_datetime.isoformat(),
              'travelType': 'single'}
    ns_response = requests.get(url, params=params, headers=d.travel_headers)
    trip = sub.TripInfo(form.cleaned_data, ns_response.text)
    default = sub.DalVrij()
    default.add(trip)
    print(default)
