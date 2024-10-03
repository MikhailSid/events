from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.locations, name='locations'),
    path('locations', views.locations, name='locations'),
    path('add_location', views.add_location, name='add_location'),
    path('<int:pk>/update_location', views.update_location.as_view(), name='update_location'),
    path('<int:pk>/delete_location', views.delete_location.as_view(), name='delete_location'),
    path('places', views.places, name='places'),
    path('add_place', views.add_place, name='add_place'),
    path('<int:pk>/update_place', views.update_place.as_view(), name='update_place'),
    path('<int:pk>/delete_place', views.delete_place.as_view(), name='delete_place'),
    path('events', views.events, name='events'),
    path('add_event', views.add_event, name='add_event'),
    path('<int:pk>/update_event', views.update_event.as_view(), name='update_event'),
    path('<int:pk>/delete_event', views.delete_event.as_view(), name='delete_event'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'), 
]