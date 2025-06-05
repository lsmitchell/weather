from django import forms

class ZipForm(forms.Form):
    zip_code = forms.CharField(label="Zip Code", max_length=5)