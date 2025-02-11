from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name="rest_home"),
    path('main/', main, name="rest_main"),
    path('order/', order, name="rest_order"),
    path('confirmation/', confirmation, name="rest_confirmation"),
]
