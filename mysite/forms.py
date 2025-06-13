from django import forms
from .models import Funeral, Donation

class FuneralForm(forms.ModelForm):
    class Meta:
        model = Funeral
        fields = ['title', 'date', 'location', 'image']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['funeral', 'donor_name', 'donation_for', 'currency', 'amount', 'payment_mode']