from django.contrib import admin
from .models import Vendor

# les champs qui vont s'afficher dans le panel d'administration pour l'entité Vendor
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approuved', 'created_at',)
    list_display_links = ('user', 'vendor_name',)

# Register your models here.
admin.site.register(Vendor, VendorAdmin)
