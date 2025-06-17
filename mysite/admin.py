from django.contrib import admin
from .models import Funeral, Donation

@admin.register(Funeral)
class FuneralAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    list_filter = ('date',)
    search_fields = ('title', 'location')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'funeral', 'amount', 'currency', 'payment_mode', 'donation_date')
    list_filter = ('funeral', 'currency', 'payment_mode')
    search_fields = ('donor_name', 'donation_for')