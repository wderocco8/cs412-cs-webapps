from typing import Any, Tuple, List
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Voter
import datetime
import plotly
import plotly.graph_objects as go


class BirthYearsContextMixin:
    """Mixin to add the appropriate birth years to context."""
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        current_year = datetime.datetime.now().year
        birth_years = range(current_year - 100, current_year - 17)  # Adults only

        context["birth_years"] = birth_years
        return context

class VoterListView(BirthYearsContextMixin, ListView):
    model = Voter
    template_name = "voter_analytics/results.html"
    context_object_name = "voters"
    paginate_by = 50

    
    
    def get_queryset(self) -> QuerySet[Any]:
        '''Limit results to small number (i.e. 25)'''
        qs = super().get_queryset()

        # Handle form submission (self.request.GET is empty if no query params sent)
        if self.request.GET:
            party = self.request.GET.get('party')
            min_birth_year = self.request.GET.get('min_birth_year')
            max_birth_year = self.request.GET.get('max_birth_year')
            voter_score = self.request.GET.get('voter_score')
            v20state = self.request.GET.get('v20state')
            v21town = self.request.GET.get('v21town')
            v21primary = self.request.GET.get('v21primary')
            v22general = self.request.GET.get('v22general')
            v23town = self.request.GET.get('v23town')
            
            # Build your query based on these parameters
            query = Voter.objects.all()
            
            if party:
                query = query.filter(party_affiliation=party)
                print(query)
            if min_birth_year:
                query = query.filter(dob__year__gte=min_birth_year)
            if max_birth_year:
                query = query.filter(dob__year__lte=max_birth_year)
            if voter_score:
                query = query.filter(voter_score=voter_score)
            if v20state:
                query = query.filter(v20state=True)
            if v21town:
                query = query.filter(v21town=True)
            if v21primary:
                query = query.filter(v21primary=True)
            if v22general:
                query = query.filter(v22general=True)
            if v23town:
                query = query.filter(v23town=True)
                
            qs = query

        return qs


class VoterDetailView(DetailView):
    model = Voter
    template_name = "voter_analytics/voter.html"
    context_object_name = "voter"


def get_voter_birth_year_distribution(voters: list[Voter]) -> Tuple[List[int], List[int]]:
    """
    Returns a tuple of 2 lists of birth years and the count of voters born in that year.
    Both lists are sorted by years in ascending order.
    """
    d = {}

    for v in voters:
        year = v.dob.year
        if year in d:
            d[year] += 1
        else:
            d[year] = 1
    
    x = sorted(d.keys())
    y = [d[year] for year in x]
    return (x, y)


def get_voter_party_affiliation(voters: list[Voter]) -> Tuple[List[int], List[int]]:
    """
    Returns a tuple of two lists.
    - x is the distinct parties
    - y is the count of voters in that party
    """
    d = {}

    for v in voters:
        party = v.party_affiliation
        if party in d:
            d[party] += 1
        else:
            d[party] = 1
    
    x = sorted(d.keys())
    y = [d[party] for party in x]
    return (x, y)


def update_voter_dict(d: dict, election: str):
    if election in d:
        d[election] += 1
    else:
        d[election] = 1
    return

def get_voter_election_distribution(voters: list[Voter]) -> Tuple[List[int], List[int]]:
    """
    Returns a tuple of two lists.
    - x is the distinct elections (sorted)
    - y is the count of voters in that voted in the corresponding election
    """
    d = {}

    for v in voters:
        v20state = v.v20state
        v21town = v.v21town
        v21primary = v.v21primary
        v22general = v.v22general
        v23town = v.v23town

        if v20state:
            election = "v20state"
            update_voter_dict(d, election)
        if v21town:
            election = "v21town"
            update_voter_dict(d, election)
        if v21primary:
            election = "v21primary"
            update_voter_dict(d, election)
        if v22general:
            election = "v22general"
            update_voter_dict(d, election)
        if v23town:
            election = "v23town"
            update_voter_dict(d, election)
        
    x = sorted(d.keys())
    y = [d[election] for election in x]
    return (x, y)


class GraphListView(BirthYearsContextMixin, ListView):
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self) -> QuerySet[Any]:
        '''Limit results to small number (i.e. 25)'''
        qs = super().get_queryset()

        # Handle form submission
        if self.request.GET:
            party = self.request.GET.get('party')
            min_birth_year = self.request.GET.get('min_birth_year')
            max_birth_year = self.request.GET.get('max_birth_year')
            voter_score = self.request.GET.get('voter_score')
            v20state = self.request.GET.get('v20state')
            v21town = self.request.GET.get('v21town')
            v21primary = self.request.GET.get('v21primary')
            v22general = self.request.GET.get('v22general')
            v23town = self.request.GET.get('v23town')
            
            # Build your query based on these parameters
            query = Voter.objects.all()
            
            if party:
                query = query.filter(party_affiliation=party)
                print(query)
            if min_birth_year:
                query = query.filter(dob__year__gte=min_birth_year)
            if max_birth_year:
                query = query.filter(dob__year__lte=max_birth_year)
            if voter_score:
                query = query.filter(voter_score=voter_score)
            if v20state:
                query = query.filter(v20state=True)
            if v21town:
                query = query.filter(v21town=True)
            if v21primary:
                query = query.filter(v21primary=True)
            if v22general:
                query = query.filter(v22general=True)
            if v23town:
                query = query.filter(v23town=True)
                
            qs = query

        return qs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        '''Handle graph creation'''
        context = super().get_context_data(**kwargs)
        voters = context['voters'] # obtain the all Voter instances
        num_voters = len(voters)

        ##################### graph 1: dob year distribution #####################
        x, y = get_voter_birth_year_distribution(voters)
        
        fig = go.Figure(
            data=[go.Bar(x=x, y=y)],
            layout=go.Layout(
                title=f'Voter Birth Year Distribution (n={num_voters})',
                xaxis_title='Birth Year',
                yaxis_title='Number of Voters',
            )
        )
        bar_div = plotly.offline.plot(
            fig,
            auto_open=False,
            output_type='div'
        )
        # add this to the context data for use in the template
        context['bar_div'] = bar_div

        ##################### graph 2: party affiliation #####################
        x, y = get_voter_party_affiliation(voters)
        
        fig = go.Figure(
            data=[go.Pie(labels=x, values=y)],
            layout=go.Layout(
                title=f'Voter distribution by party (n={num_voters})'
            )
        )
        pie_div = plotly.offline.plot(
            {'data': fig},
            auto_open=False,
            output_type='div'
        )
        # add this to the context data for use in the template
        context['pie_div'] = pie_div


        ##################### graph 3: election voter distribution #####################
        x, y = get_voter_election_distribution(voters)
        
        fig = go.Figure(
            data=[go.Bar(x=x, y=y)],
            layout=go.Layout(
                title=f'Voter Count by Election (n={num_voters})',
                xaxis_title='Election',
                yaxis_title='Number of Voters',
            )
        )
        election_bar_div = plotly.offline.plot(
            fig,
            auto_open=False,
            output_type='div'
        )
        # add this to the context data for use in the template
        context['election_bar_div'] = election_bar_div


        return context