from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class ProfileContextMixin:
    """Mixin to add the current user's profile to the context."""
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the user's profile if they are authenticated
        context["profile"] = Profile.objects.get(user=self.request.user) if self.request.user.is_authenticated else None
        return context
    

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        # Override the default login URL with a custom one
        return reverse("login")

class ShowAllProfilesListView(ProfileContextMixin, ListView):
    """List all profiles"""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


class ShowProfilePageDetailView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile_page.html"
    context_object_name = "profile"


class CreateProfileView(ProfileContextMixin, CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        # Create UserCreationForm instance from POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Check if the user_form is valid
        if user_form.is_valid():
            # Save the user and get the user instance
            user = user_form.save()
            
            # Attach the user to the Profile instance
            profile = form.save(commit=False)
            profile = form.instance # *could* do this, but is not safe (doesn't perform validation before creating a new user)
            profile.user = user
            
            # Save the profile instance
            profile.save()
            
            # Optionally, log the user in after registration
            # from django.contrib.auth import login
            # login(self.request, user)

            return super().form_valid(form)  # Call the superclass' form_valid method
        
        return self.form_invalid(form)


# NOTE: not sure why this works without ProfileContextMixin
class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    # def get_success_url(self):
    #     return self.object.get_absolute_url()

    def get_object(self) -> Model:
        return Profile.objects.get(user=self.request.user) # NOTE: we CANNOT match by pk here...


class CreateStatusMessageView(ProfileContextMixin, CustomLoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     # used to grab the pk from the url parameters
    #     # profile_pk = self.kwargs['pk']
    #     # profile = Profile.objects.get(pk=profile_pk)
    #     profile = self.get_object()

    #     # create context and add profile
    #     context = super().get_context_data(**kwargs)
    #     context['profile'] = profile
    #     return context
    
    def form_valid(self, form):
        # profile = Profile.objects.get(pk=self.kwargs['pk'])
        profile = self.get_object()
        form.instance.profile = profile
        # This line is not needed since we included `auto_add_now` in the StatusMessage.timestamp field
        # form.instance.timestamp = timezone.now()

        # save the status message to db
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        # for each file create an Image object and set the fk to sm (StatusMessage)
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        # use the `profile` object associated with this StatusMessage to re-route
        return self.object.profile.get_absolute_url()
    
    def get_object(self) -> Model:
        return Profile.objects.get(user=self.request.user)
    

class StatusMessageDeleteView(ProfileContextMixin, CustomLoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_success_url(self) -> str:
        # use the `profile` object associated with this StatusMessage to re-route
        return self.object.profile.get_absolute_url()

        
class StatusMessageUpdateView(ProfileContextMixin, CustomLoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status_message"

    def get_success_url(self) -> str:
        # use the `profile` object associated with this StatusMessage to re-route
        return self.object.profile.get_absolute_url()
    

class CreateFriendView(CustomLoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
         # Get the profiles based on the URL parameters
        profile_pk = self.get_object().pk
        other_profile_pk = self.kwargs.get('other_pk')
        
        # Find the profiles
        profile = Profile.objects.get(pk=profile_pk)
        other_profile = Profile.objects.get(pk=other_profile_pk)

        # Add the other profile as a friend
        profile.add_friend(other_profile)

        # Redirect back to the original profile's page
        return redirect(profile.get_absolute_url())
    
    def get_object(self) -> Model:
        return Profile.objects.get(user=self.request.user)
    

class ShowFriendSuggestionsView(CustomLoginRequiredMixin, DetailView):
    """List all friend suggestions"""
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self) -> Model:
        return Profile.objects.get(user=self.request.user)


class NewsFeedDetailView(CustomLoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self) -> Model:
        return Profile.objects.get(user=self.request.user)
