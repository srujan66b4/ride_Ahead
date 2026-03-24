"""
URL configuration for rideahead project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rides import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('rider/', views.rider_registration, name='rider_registration'),
    path('book/', views.book_ride, name='book_ride'),
    path('confirmation/', views.ride_confirmation, name='confirmation'),
    path('tommy/', views.thank_you, name='tommy'),
    path('bunny/', views.book_ride, name='bunny'),
    path('driver-rides/', views.driver_rides, name='driver_rides'),
    path('my-rides/', views.user_rides, name='user_rides'),
    path('ride/<int:ride_id>/', views.user_ride_details, name='user_ride_details'),
    path('accept-ride/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('reject-ride/<int:ride_id>/', views.reject_ride, name='reject_ride'),
    path('profile/', views.profile, name='profile'),
    path('driver-login/', views.driver_login, name='driver_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
