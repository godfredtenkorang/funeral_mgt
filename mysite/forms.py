from django import forms
from .models import Funeral, Donation
from django.utils import timezone

class FuneralForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )

    class Meta:
        model = Funeral
        fields = ['title', 'date', 'location', 'image']

class DonationForm(forms.ModelForm):
    donation_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )

    class Meta:
        model = Donation
        fields = ['funeral', 'donor_name', 'donation_for', 'currency', 'amount', 'payment_mode', 'donation_date']