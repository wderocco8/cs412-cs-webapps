from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Result

class ResultListView(ListView):
    model = Result
    template_name = "marathon/results.html"
    context_object_name = "results"
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        '''Limit results to small number (i.e. 25)'''
        qs = super().get_queryset()

        # handle search form/URL parameters:
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            qs = Result.objects.filter(city__icontains=city)

        return qs
