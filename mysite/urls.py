from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='admin_dashboard'),
    # Funeral URLs
    path('funeral_list/', views.FuneralListView.as_view(), name='funeral_list'),
    path('add/', views.FuneralCreateView.as_view(), name='funeral_add'),
    path('<int:pk>/', views.FuneralDetailView.as_view(), name='funeral_detail'),
    
    
    # Donation URLs
    path('<int:funeral_id>/donation/add/', views.DonationCreateView.as_view(), name='donation_add'),
    path('<int:funeral_id>/report/', views.donation_report, name='donation_report'),
    path('<int:funeral_id>/export/', views.export_donations_excel, name='export_donations'),
    path('donations/<int:pk>/receipt/', views.DonationReceiptView.as_view(), name='view_receipt'),
    path('donations/<int:donation_id>/pdf/', views.download_receipt_pdf, name='download_receipt_pdf'),
    path('<int:donation_id>/export-pdf/', views.export_donations_pdf, name='export_donations_pdf'),

]