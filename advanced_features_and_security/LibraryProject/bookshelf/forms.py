from django import forms

class ExampleForm(forms.Form):
    q = forms.CharField(max_length=200, required=False)