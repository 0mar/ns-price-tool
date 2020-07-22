from django.shortcuts import render
from pricing.models import Station
from datetime import datetime
from .forms import TripForm
from django.forms import formset_factory
import pricing.data as d
import requests
import pricing.subscriptions as sub
import sys
from django_tables2 import SingleTableView
from .tables import SubscriptionTable

if sys.version_info.minor < 6:
    raise SystemError("Need at least Python 3.6, found %s" % sys.version)

# Create your views here.

TripFormSet = formset_factory(TripForm, extra=3)


def index(request):
    stations = [str(station) for station in Station.objects.all()]
    station_str = '[\"%s\"]' % '\",\"'.join(stations)
    context = {'stations': station_str}
    if request.method == 'POST':
        formset = TripFormSet(request.POST)
        context['formset'] = formset
        if formset.is_valid():
            subscriptions = get_prices(formset)
            table_data = generate_table_data(subscriptions)
            table = SubscriptionTable(table_data)
            context['table'] = table
            best_sub = subscriptions[0]
            prices = best_sub.marginal_prices()
            for i, form in enumerate(formset):
                form.fields['price'].widget.attrs['value'] = "€%.2f" % prices[i]
                # from IPython import embed
                # embed()
            return render(request, 'index.html', context)
    else:
        formset = TripFormSet()
        context['formset'] = formset
    return render(request, "index.html", context)


def get_prices(formset):
    subs = [sub.Basis(), sub.DalVoordeel(), sub.WeekendVoordeel, sub.AltijdVoordeel(), sub.DalVrij(), sub.WeekendVrij(),
            sub.AltijdVrij()]
    trip_list = []
    for form in formset:
        dep_code = Station.objects.get(long=form.cleaned_data['departure']).code
        arr_code = Station.objects.get(long=form.cleaned_data['arrival']).code
        dep_datetime = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
        url = 'https://gateway.apiportal.ns.nl/public-prijsinformatie/prices'
        params = {'fromStation': dep_code, 'toStation': arr_code, 'plannedFromTime': dep_datetime.isoformat(),
                  'travelType': 'single'}
        ns_response = requests.get(url, params=params, headers=d.travel_headers)
        trip = sub.TripInfo(form.cleaned_data, ns_response.text)
        trip_list.append(trip)
        for sub_entry in subs:
            sub_entry.add(trip)
    best_subs = sorted(subs, key=lambda x: x.total_price())
    return best_subs


def generate_table_data(subs):
    table_data = []
    for sub_entry in subs:
        data = {'name': sub_entry.name, 'base_price': sub_entry.euro_repr(sub_entry.base_price()),
                'trip_prices': sub_entry.euro_repr(sub_entry.marginal_price()),
                'total_price': sub_entry.euro_repr(sub_entry.total_price())}
        table_data.append(data)
    return table_data


class PersonListView(SingleTableView):
    table_class = SubscriptionTable
    template_name = 'templates/subscriptions.html'
