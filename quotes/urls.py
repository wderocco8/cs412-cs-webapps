from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('quote/<int:pk>', QuotePageView.as_view(), name="quote"),
    path('person/<int:pk>', PersonPageView.as_view(), name="person"),
    path('random', RandomQuotePageView.as_view(), name="random"),
    path('about/', AboutPageView.as_view(), name="about"),
]
