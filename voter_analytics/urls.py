from django.urls import path
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name="voter_home"),
    path('voter/<int:pk>', VoterDetailView.as_view(), name="voter"),
    path('graphs/', GraphListView.as_view(), name="voter_graphs"),
]
