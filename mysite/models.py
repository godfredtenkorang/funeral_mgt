from django.db import models
from django.utils import timezone
from django.urls import reverse

class Funeral(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='funeral_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('funeral_detail', kwargs={'pk': self.pk})

class Donation(models.Model):
    PAYMENT_MODES = [
        ('cash', 'Cash'),
        ('momo', 'Mobile Money'),
        ('cheque', 'Cheque'),
    ]

    CURRENCIES = [
        ('GHS', 'Ghana Cedis (GHS)'),
        ('USD', 'US Dollars (USD)'),
        ('EUR', 'Euros (EUR)'),
        ('GBP', 'British Pounds (GBP)'),
    ]

    funeral = models.ForeignKey(Funeral, on_delete=models.CASCADE, related_name='donations')
    donor_name = models.CharField(max_length=200)
    donation_for = models.CharField(max_length=200)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='GHS')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES)
    donation_date = models.DateTimeField(default=timezone.now)
    ecobank_logo = models.ImageField(default='ecobank_logo.png')
    fnet_logo = models.ImageField(default='fnet_logo.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"

    class Meta:
        ordering = ['-donation_date']