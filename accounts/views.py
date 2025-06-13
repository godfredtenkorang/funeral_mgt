from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from accounts.models import User

def register(request):
    return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
       
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            
            
            return redirect("admin_dashboard")

            
        else:
            messages.error(request, 'Invalid password.')
            return redirect('login')
        
        
    return render(request, 'accounts/login.html')


# def register(request):
#     if request.method == 'POST':
        
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False # Deactivate account until OTP is verified
#             user.save()
            
#             messages.success(request, 'Registration succss.')
#             return redirect('verify_registration_otp')
#         else:
#             messages.error(request, 'Registration failed. Please correct the errors below.')
    
        
#     context = {
#         'form': form
#     }
#     return render(request, 'users/register.html', context)


