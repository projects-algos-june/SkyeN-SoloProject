from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('logreg', views.logreg),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('order', views.order),
    path('checkout', views.checkout),
]