from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TripForm(forms.Form):
    departure = forms.CharField(label='Departure', max_length=50,
                                widget=forms.TextInput(attrs={'class': 'station_input'}))
    arrival = forms.CharField(label='Arrival', max_length=50,
                              widget=forms.TextInput(attrs={'class': 'station_input'}))
    date = forms.DateField(label='Select Date', input_formats=['%d-%m-%Y'])
    time = forms.TimeField(label='Select Time')
    price = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': "form-control-plaintext"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'inline_field.html'
