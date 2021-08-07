from django.urls import path, include
from . import views
from django.conf.urls import include, re_path
from django.urls.conf import include
from rest_framework import routers
from datum.views import ProfileViewSet, UserViewSet, PreferenceViewsSet, InterestViewsSet, MatchViewsSet, HomepageView, ProfileDetailView, UserDetailView, UserListView, UserLoginView, ProfileUpdateView, PreferenceUpdateView, DashboardView, UserMatchesListView
from django.urls import path
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'preferences', views.PreferenceViewsSet)
router.register(r'interests', views.InterestViewsSet)
router.register(r'matches', views.MatchViewsSet)


app_name = 'datum'

urlpatterns = [

    path('api/', include(router.urls)),

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
