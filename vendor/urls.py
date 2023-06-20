from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    path('registerVendor/', views.registerVendor, name="registerVendor"),
]