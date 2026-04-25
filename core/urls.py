"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('apps.products.urls')),
    path('', include('apps.users.urls')),
    path('', lambda request: redirect('products:list')),
]
