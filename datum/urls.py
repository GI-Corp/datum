from django.urls import path, include
from . import views
from django.conf.urls import include, re_path
from .views import HomepageView, ProfileDetailView, UserDetailView, UserListView, UserLoginView, ProfileUpdateView, PreferenceUpdateView, DashboardView, UserMatchesListView

app_name = 'datum'

urlpatterns = [
    
    path('', views.DashboardView.as_view(), name='index'),
    path("your_matches/", views.UserMatchesListView.as_view(), name="matches"),

    path('users/', views.UserListView.as_view(), name='users' ),
    path('user_create/', views.UserCreateView.as_view(), name='user_create'),
    path('user_details/<int:pk>', views.UserDetailView.as_view(), name='user'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    path('profile_details/<int:pk>', views.ProfileDetailView.as_view(), name='profile'),
    path('update_profile/<int:pk>', views.ProfileUpdateView.as_view(), name='update_profile'),

    path('preference_details/<int:pk>', views.PreferenceDetailView.as_view(), name='preference'),
    path('update_preference/<int:pk>', views.PreferenceUpdateView.as_view(), name='update_preference'),


]
