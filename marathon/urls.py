from django.urls import path
from .views import *

urlpatterns = [
    path('', ResultListView.as_view(), name="marathon_home"),
    path('results', ResultListView.as_view(), name="marathon_results")
]
