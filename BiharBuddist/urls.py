 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path('api/user/', include('user.urls')),
    path('user/', include('contactUs.urls')),
    path('link/', include('officialLinks.urls')),
    path('gallery/', include('gallery.urls')),
    path('tourist/', include('tourism.urls')),
    path('overview/', include('overview.urls')),
]
 
