from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    profile_image_url = models.URLField()

    
    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'
    
    def get_status_messages(self):
        return StatusMessage.objects.all().filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile_page', kwargs={"pk": self.pk})
    
    def get_friends(self):
        friend_obs = Friend.objects.all().filter(Q(profile1=self) | Q(profile2=self))
        friends = [friend.profile1 if friend.profile2 == self else friend.profile2 for friend in friend_obs]
        return friends
    
    def add_friend(self, other):
        friends = Friend.objects.all().filter(Q(profile1=self) | Q(profile2=self))
        for friend in friends:
            if friend.profile1 == self and friend.profile2 == other:
                return
            elif friend.profile1 == other and friend.profile2 == self:
                return

        # if made it here (not yet friends)
        friend = Friend(profile1=self, profile2=other)
        friend.save()
        return

    def get_friend_suggestions(self):
        profiles = Profile.objects.all()
        friend_obs = Friend.objects.all().filter(Q(profile1=self) | Q(profile2=self))
        suggestions = []
        for profile in profiles:
            if profile == self:
                continue
            
            isNew = True
            
            for friend in friend_obs:
                if profile == friend.profile1 or profile == friend.profile2:
                    isNew = False
                    break

            if isNew:
                suggestions.append(profile)

        return suggestions
    
    # optimized version (from chat)
    # def get_friend_suggestions(self):
    #     # Get profiles that are not the current user and are not already friends
    #     friend_ids = Friend.objects.filter(Q(profile1=self) | Q(profile2=self)).values_list('profile1', 'profile2')
        
    #     # Flatten the tuple list to get a single list of friend IDs
    #     friend_ids = {pk for p1, p2 in friend_ids for pk in [p1, p2]}
        
    #     # Exclude current user and their friends from the suggestion list
    #     suggestions = Profile.objects.exclude(pk__in=friend_ids).exclude(pk=self.pk)
        
    #     return suggestions

    def get_news_feed(self):
        friends = self.get_friends()

        # Include the current profile in the list to get their own status messages too
        profiles = [self] + friends

        # Retrieve all status messages for the current profile and their friends, ordered by timestamp
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
        
        return news_feed

    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(to="Profile", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.message}'
    
    def get_images(self):
        return Image.objects.all().filter(status_message=self).order_by('-timestamp')


class Image(models.Model):
    image_file = models.ImageField(upload_to='mini_fb/')
    status_message = models.ForeignKey(to="StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True, null=True)


class Friend(models.Model):
    profile1 = models.ForeignKey(to="Profile", on_delete=models.CASCADE, related_name="friends_as_profile1")
    profile2 = models.ForeignKey(to="Profile", on_delete=models.CASCADE, related_name="friends_as_profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.profile1.firstname} {self.profile1.lastname} & {self.profile2.firstname} {self.profile2.lastname}'