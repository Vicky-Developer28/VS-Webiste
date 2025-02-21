from django.contrib import admin
from django.urls import path
from .models import Carousel, Feature, Service
from django.contrib import admin
from .models import contact_enquiry

@admin.register(contact_enquiry)
class contact_enquiry(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'service_type', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
