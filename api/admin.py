from django.contrib import admin
from .models import User, Donation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'attempted_at')
    list_filter = ('status',)
