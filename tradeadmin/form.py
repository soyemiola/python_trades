from django import forms

class NewTrader(forms.Form):
    firstname = forms.CharField(required=True, label="Firstname", widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(required=True, label="Lastname", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    stock = forms.CharField(required=True, label="Stock Value", widget=forms.TextInput(attrs={'class': 'form-control'}))

    