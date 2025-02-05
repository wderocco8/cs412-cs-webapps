from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
import random

class HomePageView(ListView):
    model = Quote
    template_name = "quotes/home.html"
    context_object_name = "quotes"


class RandomQuotePageView(DetailView):
    """Shows a single quote object"""
    model = Quote
    template_name = "quotes/quote.html"
    context_object_name = "quote"

    def get_object(self) -> Model:
        """Overrides inheritted method (get one random quote)"""
        quotes = Quote.objects.all()
        quote = random.choice(quotes)
        return quote
    
class QuotePageView(DetailView):
    """Shows a single quote object"""
    model = Quote
    template_name = "quotes/quote.html"
    context_object_name = "quote"


class PersonPageView(DetailView):
    '''Show all quotes and all images for one person.'''
    model = Person
    template_name = 'quotes/person.html'
    context_object_name = 'person'


class AboutPageView(TemplateView):
    template_name = "quotes/about.html"