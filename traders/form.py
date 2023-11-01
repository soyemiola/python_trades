from django import forms

class TraderLogin(forms.Form):
    email = forms.EmailField(required=True, label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
