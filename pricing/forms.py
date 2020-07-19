from django import forms

class TripForm(forms.Form):
    departure = forms.CharField(label='Departure', max_length=50)
    arrival = forms.CharField(label='Arrival', max_length=50)
    date = forms.DateField(label='Select Date')
    time = forms.TimeField(label='Select Time')