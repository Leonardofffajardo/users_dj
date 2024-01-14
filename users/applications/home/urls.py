from django.urls import path

from . import views

app_name = "home_app"

urlpatterns = [
    path('panel/', 
         views.homepage.as_view(), 
         name='panel'),
    path('mixin/', 
         views.HomeDate.as_view(), 
         name='mixin'),
]