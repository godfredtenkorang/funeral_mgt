import os
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Funeral, Donation
from .forms import FuneralForm, DonationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
import xlwt

from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import send_donation_sms, send_donation_thanksgiving_sms



def index(request):
    funerals = Funeral.objects.all()[:5]
    context = {
        'funerals': funerals
    }
    return render(request, 'mysite/index.html', context)

# Funeral Views
class FuneralListView(LoginRequiredMixin, ListView):
    model = Funeral
    template_name = 'mysite/funeral_list.html'
    context_object_name = 'funerals'
    ordering = ['-date']
    
class FuneralCreateView(LoginRequiredMixin, CreateView):
    model = Funeral
    form_class = FuneralForm
    template_name = 'mysite/funeral_form.html'
    success_url = reverse_lazy('funeral_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Funeral added successfully!')
        return super().form_valid(form)
    
class FuneralDetailView(LoginRequiredMixin, DetailView):
    model = Funeral
    template_name = 'mysite/funeral_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = self.object.donations.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        donation_id = request.POST.get('donation_id')
        
        try:
            donation = self.object.donations.get(id=donation_id)
            send_donation_thanksgiving_sms(
                phone_number=donation.phone_number,
                donor_name=donation.donor_name
            )
            messages.success(request, f"SMS sent successfully to {donation.donor_name}")
        except Donation.DoesNotExist:
            messages.error(request, "Donation not found")
        except Exception as e:
            messages.error(request, f"Failed to send SMS: {str(e)}")
        
        return redirect('funeral_detail', pk=self.object.pk)
    
    
    
class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'mysite/donation_form.html'
    
    def get_success_url(self):
        return reverse_lazy('funeral_detail', kwargs={'pk': self.object.funeral.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
         # Send SMS notification after successful form submission
        
        donation = self.object
        send_donation_sms(
            phone_number=donation.phone_number,
            donor_name=donation.donor_name,
            donation_for=donation.funeral.title,
            
        )
        
        messages.success(self.request, 'Donation recorded successfully!')
        return response
    
    
class DonationReceiptView(DetailView):
    model = Donation
    template_name = 'mysite/print_receipt.html'
    context_object_name = 'donation'
    
    
def download_receipt_pdf(request, donation_id):
    donation = Donation.objects.get(id=donation_id)
    
    template = get_template('mysite/print_receipt.html')
    html = template.render({'donation': donation})
    result = HttpResponse(content_type='application/pdf')
    # Create a link callback function
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        # Handle static files
        if uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
        # Handle media files
        elif uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
        # Handle absolute URIs
        else:
            return uri

        # Make sure the file exists
        if not os.path.isfile(path):
            raise Exception(f"Media file not found: {path}")
        
        return path
    
    pisa_status = pisa.CreatePDF(html, dest=result, link_callback=link_callback, encoding='UTF-8')
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return result
    
    
    
def donation_report(request, funeral_id):
    funeral = get_object_or_404(Funeral, pk=funeral_id)
    donations = funeral.donations.all()
    
    # Summary data
    total_donations = donations.aggregate(total=Sum('amount'))['total'] or 0
    currency_totals = donations.values('currency').annotate(total=Sum('amount'))
    
    context = {
        'funeral': funeral,
        'donations': donations,
        'total_donations': total_donations,
        'currency_totals': currency_totals,
    }
    
    return render(request, 'mysite/donation_report.html', context)

def export_donations_pdf(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)
    
    template_path = 'mysite/donation_template.html'
    context = {'donation': donation}
    
    # Render template
    template = get_template(template_path)
    html = template.render(context)
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="donation_receipt_{donation.id}.pdf"'
    
    # Generate PDF
    pdf_status = pisa.CreatePDF(
        html,
        dest=response,
        encoding='UTF-8',
        link_callback=lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, '')))
    
    if pdf_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

def export_donations_excel(request, funeral_id):
    funeral = get_object_or_404(Funeral, pk=funeral_id)
    donations = funeral.donations.all()
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{funeral.title}_donations.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Donations')
    
     # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Donor Name', 'Donation For', 'Amount', 'Currency', 'Payment Mode', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    
    for donation in donations:
        row_num += 1
        ws.write(row_num, 0, donation.donor_name, font_style)
        ws.write(row_num, 1, donation.donation_for, font_style)
        ws.write(row_num, 2, str(donation.amount), font_style)
        ws.write(row_num, 3, donation.currency, font_style)
        ws.write(row_num, 4, donation.get_payment_mode_display(), font_style)
        ws.write(row_num, 5, donation.donation_date.strftime('%Y-%m-%d %H:%M'), font_style)
    
    # Add summary
    row_num += 2
    ws.write(row_num, 0, 'Summary', font_style)
    
    currency_totals = donations.values('currency').annotate(total=Sum('amount'))
    for total in currency_totals:
        row_num += 1
        ws.write(row_num, 0, f"Total {total['currency']}:", font_style)
        ws.write(row_num, 1, str(total['total']), font_style)
    
    row_num += 1
    ws.write(row_num, 0, "Grand Total:", font_style)
    ws.write(row_num, 1, str(donations.aggregate(total=Sum('amount'))['total'] or 0), font_style)
    
    wb.save(response)
    return response