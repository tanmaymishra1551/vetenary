from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/', include('app_name.urls')),  # Replace 'your_app_name' with the actual app name
]
