from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    """A specialized version of TemplateView to display our home page."""
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
    """Display our about page."""
    template_name = "pages/about.html"

class SchedulePageView(TemplateView):
    """Display our schedule page."""
    template_name = "pages/schedule.html"
