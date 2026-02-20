from django.contrib import admin
from django.core.mail import send_mail
from .models import User, Society, Flat, MaintenanceBill
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.action(description='Set selected users as active')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description='Set selected users as inactive')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.action(description='Send credentials via console email')
def send_credentials(modeladmin, request, queryset):
    for user in queryset:
        # Ideally generate/reset password; here we assume password present or set a temp one
        # For demo, we will send username only
        send_mail(
            subject='Your Society Management credentials',
            message=f"Hi {user.username},\nYour account is created. Username: {user.username}",
            from_email='admin@society.local',
            recipient_list=[user.email],
        )
    modeladmin.message_user(request, "Emails sent to selected users (console).")
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    actions = [make_active, make_inactive, send_credentials]

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ('flat_number', 'society', 'owner')

@admin.register(MaintenanceBill)
class MaintenanceBillAdmin(admin.ModelAdmin):
    list_display = ('flat', 'month', 'amount', 'status')
