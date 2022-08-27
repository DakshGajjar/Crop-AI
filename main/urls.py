from django.contrib import admin
from django.urls import path,include
from main import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('help',views.help,name='help'),
    path('croprec',views.croprec,name='crop recommender'),
    path('cropdis',views.cropdis,name='crop disease detector'),
    path('cropyield',views.cropyield,name='crop yield estomator'),
    path('pests',views.pests,name = 'crop pests identifier')
]