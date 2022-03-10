from django import forms


class AvailabilityForm(forms.Form):
    move_in = forms.DateTimeField(
        required=True,
        input_formats=['%d/%m/%Y %H:%M', ]
    )
    move_out = forms.DateTimeField(
        required=True,
        input_formats=['%d/%m/%Y %H:%M', ]
    )
