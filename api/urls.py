from django.urls.conf import include
from rest_framework import routers
from api.views import ProfileViewSet, UserViewSet, PreferenceViewsSet, InterestViewsSet, MatchViewsSet
from django.urls import path
from api import views
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'preferences', views.PreferenceViewsSet)
router.register(r'interests', views.InterestViewsSet)
router.register(r'matches', views.MatchViewsSet)

urlpatterns = [
    path('', include(router.urls)),
]

