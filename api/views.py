from datetime import datetime
from api.serializers import ProfileSerializer
from django.db.models import manager
from django.http import HttpResponse, JsonResponse, Http404, request
from django.views.decorators.csrf import csrf_exempt
from rest_framework import renderers, views
from rest_framework.parsers import JSONParser
from datum.models import User, Profile, Preference, Interest, Match
from api.serializers import UserSerializer, PreferenceSerializer, ProfileSerializer, InterestSerializer, MatchSerializer
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import viewsets
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class PreferenceViewsSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class InterestViewsSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MatchViewsSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    





    