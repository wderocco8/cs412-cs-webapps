from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    # optional : define specific behavior for this form (i.e. type of inputs)
    # first_name = forms.CharField(label="First Name", required=True)
    # firstname
    # lastname
    # city
    # email_address
    # profile_image_url

    class Meta:
        model = Profile
        exclude = ['user']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['firstname', 'lastname']

        
class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        exclude = ['profile']


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']