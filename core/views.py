from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import Flat, MaintenanceBill
from .models import User



def login_view(request):
    # If already logged in, send directly to dashboard
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'OWNER':
            return redirect('owner_dashboard')
        elif request.user.role == 'TENANT':
            return redirect('tenant_dashboard')

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        identifier = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']

        # Try login with username
        user = authenticate(request, username=identifier, password=password)

        # If not found, try email
        if not user:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user and user.is_active:
            login(request, user)

            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'OWNER':
                return redirect('owner_dashboard')
            elif user.role == 'TENANT':
                return redirect('tenant_dashboard')
        else:
            messages.error(request, "Invalid credentials or inactive account.")

    return render(request, 'core/login.html', {'form': form})

# def redirect_to_role_dashboard(user):
#     if user.role == 'ADMIN':
#         return redirect('admin_dashboard')
#     elif user.role == 'OWNER':
#         return redirect('owner_dashboard')
#     elif user.role == 'TENANT':
#         return redirect('tenant_dashboard')
#     return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('login')
    return render(request, 'core/admin_dashboard.html')

@login_required
def owner_dashboard(request):
    if request.user.role != 'OWNER':
        return redirect('login')
    # example: owner -> their flat and bills
    try:
        flat = Flat.objects.get(owner=request.user)
        bills = MaintenanceBill.objects.filter(flat=flat)
    except Flat.DoesNotExist:
        flat = None
        bills = []
    return render(request, 'core/owner_dashboard.html', {'flat': flat, 'bills': bills})

@login_required
def tenant_dashboard(request):
    if request.user.role != 'TENANT':
        return redirect('login')
    return render(request, 'core/tenant_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
