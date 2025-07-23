from django.contrib import admin
from .models import Outlet, EmployeeProfile

@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    search_fields = ('name',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'emp_code', 'contact_number', 'outlet')
    search_fields = ('user__username', 'emp_code', 'first_name', 'last_name')
    list_filter = ('outlet',)
