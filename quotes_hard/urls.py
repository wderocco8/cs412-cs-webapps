from django.urls import path
from .views import HomePageView, QuotePageView, ShowAllPageView, AboutPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home_qh"),
    path('quote/', QuotePageView.as_view(), name="quote_qh"),
    path('show_all/', ShowAllPageView.as_view(), name="all_qh"),
    path('about/', AboutPageView.as_view(), name="about_qh"),
]
