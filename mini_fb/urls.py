from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ShowAllProfilesListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageDetailView.as_view(), name="show_profile_page"),
    path('status/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),

    path('status/<int:pk>/delete', StatusMessageDeleteView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', StatusMessageUpdateView.as_view(), name="update_status"),
    
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="add_friend"),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/news_feed', NewsFeedDetailView.as_view(), name="news_feed"),

    path('login', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name="logout"),

]
