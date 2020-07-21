from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TripForm(forms.Form):
    departure = forms.CharField(label='Departure', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'station_input'}))
    arrival = forms.CharField(label='Arrival', max_length=50,
                              widget=forms.TextInput(attrs={'class': 'station_input'}))
    date = forms.DateField(label='Select Date', input_formats=['%d-%m-%Y'])
    # date = forms.DateField(label='Select Date')
    time = forms.TimeField(label='Select Time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_trip_form'
        self.helper.form_class = 'form_class'
        self.helper.add_input(Submit('submitit', 'Submit Form'))
