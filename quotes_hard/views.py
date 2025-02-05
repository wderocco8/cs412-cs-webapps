from django.shortcuts import render
from django.views.generic import TemplateView
import random

# global variables (eventually will use django models here...)
quotes = [
    "I took a test once; they said I was a genius.",
    "I love red bell peppers. Bell peppers in general, really. I like to eat them like apples. They're so crunchy and delicious.",
    "My comfort zone is like a little bubble around me, and I've pushed it in different directions and made it bigger and bigger until these objectives that seemed totally crazy eventually fall within the realm of the possible.",
]

images = [
    "https://cdn-images-1.medium.com/max/853/1*p1jT_VTy6PDDOcX2myFKnQ.jpeg",
    "https://tb12sports.com/cdn/shop/articles/freesolo-13cwcut-1548767208-e1629304616381.jpg?v=1632318226&width=1024",
    "https://i.ytimg.com/vi/ncDFDz9k35o/maxresdefault.jpg",
]

class HomePageView(TemplateView):
    template_name = "quotes_hard/home.html"
    
    # Override get_context_data to pass the quotes and images to the template
    def get_context_data(self, **kwargs):
        # Get the base context
        context = super().get_context_data(**kwargs)
        
        # Add custom data to the context
        context['quote'] = random.choice(quotes)
        context['image'] = random.choice(images)
        
        return context


class QuotePageView(TemplateView):
    template_name = "quotes_hard/quote.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['quote'] = random.choice(quotes)
        context['image'] = random.choice(images)
        
        return context
    

class ShowAllPageView(TemplateView):
    template_name = "quotes_hard/show_all.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['quote_image_pairs'] = zip(quotes, images)        
        return context


class AboutPageView(TemplateView):
    template_name = "quotes_hard/about.html"