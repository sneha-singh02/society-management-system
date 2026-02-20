from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('tenant-dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
]
