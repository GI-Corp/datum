from os import stat
from urllib.parse import urlparse
from django.contrib import auth, messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.context_processors import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.base import Model
from django.db.models.query_utils import select_related_descend
from django.forms.models import ModelForm
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse, reverse_lazy
from django.utils.timezone import deactivate
from django.views.generic import CreateView, DetailView
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.views.generic.list import ListView

from datum.forms import PreferenceForm, ProfileForm, UserForm, UserLoginForm
from datum.models import Interest, Match, Preference, Profile
from datum.mixins import ProfileUpdatePermissionMixin, PreferenceUpdatePermissionMixing
from django.db.models import Q

from django.contrib.auth import authenticate, login
from rest_framework import authentication
from rest_framework import response
from datum.permissions import (
    MatchAccessPermission,
    UserAccessPermission, 
    ProfileAccessPermission, 
    PreferenceAccessPermission,
    InterestAccessPermission,
    )
from datetime import datetime
from django.db.models import manager, query
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import renderers, views
from rest_framework.parsers import JSONParser
from datum.serializers import (
    UserSerializer,
    LoginSerializer, 
    PreferenceSerializer, 
    ProfileSerializer, 
    InterestSerializer, 
    MatchSerializer,
    ProfileSerializerRestricted,
    )
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = 'test/test.html'
    login_url = 'datum:login'

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'test/user_list.html'
    context_object_name = 'users'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'test/user_details.html'
    context_object_name = 'user'

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'test/user_create.html'
    success_message = 'Success, user is registered'
    success_url = reverse_lazy('datum:login')

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'test/login.html'
    success_message = 'You are logged in'
    success_url = reverse_lazy('datum:index')

class UserLogoutView(SuccessMessageMixin, LogoutView):
    success_message = 'You are logged out'
    next_page = reverse_lazy('datum:login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'test/profile_create.html'
    success_url = reverse_lazy('datum:index')    

class PreferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Preference
    form_class = PreferenceForm
    template_name = 'test/update_preference.html'
    success_url = reverse_lazy('datum:index')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'test/profile_details.html'
    context_object_name = 'profile'

class PreferenceDetailView(LoginRequiredMixin, DetailView):
    model = Preference
    template_name = 'test/preference_details.html'
    context_object_name = 'preference'

class DashboardView(LoginRequiredMixin, ListView, TemplateView, View):
    model = Profile
    template_name = 'test/test.html'
    context_object_name = 'profiles'

    def post(self, *args, **kwargs):
        resulting_matches = self.matches(self, request)
        if request.POST.get('Skip') == 'Skip':
                matches = resulting_matches.exclude(user=request.POST.get('profile'))
                your_partner = request.POST.get('profile')
                self.your_matches(self, request, your_partner, status=False)

        if request.POST.get('Like') == 'Like':
            your_partner = request.POST.get('profile')
            self.your_matches(self, request, your_partner, status=True)

        check_for_matches = Match.objects.filter(
            current_user=self.request.user, 
            user_requested__in=resulting_matches
            ).values_list('user_requested', flat=True)

        num_of_excluded = len(check_for_matches)
        print(f'Number of excluded profiles (already exist): {num_of_excluded}')
        print(f'Matches (already exist):  {check_for_matches}')

        matches = matches.exclude(user_requested__in=check_for_matches)
        return matches

        # return super().get(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.matches(self, request)
        return super().get(request, *args, **kwargs)

    def matches(self, *args, **kwargs):
        current_user = self.request.user
        current_user_interest = Profile.objects.filter(user=current_user).values_list('interest', flat=True)

        users_by_interest = Profile.objects.filter(
            interest__in=current_user_interest
            ).exclude(
                id=current_user.profile.id
                ).values_list('user', flat=True).distinct()

        users_by_age = Profile.objects.filter(
            birthdate__lte=current_user.user_preference.get_min_date(), 
            birthdate__gte=current_user.user_preference.get_max_date()
        ).exclude(id=current_user.profile.id).values_list('user', flat=True).distinct()

        resulting_match = set(users_by_interest).intersection(set(users_by_age))
        
        num_users = len(resulting_match)
        print(f'final matches for {current_user}: {resulting_match}')

        matches = Profile.objects.filter(user__in=resulting_match)
        return matches
        
    def your_matches(self, request, your_partner, status):
        partner = User.objects.get(id=self.your_partner.id)
        if status:
            match_established = Match.objects.get_or_create(
                current_user=self.request.user, 
                user_requested=partner, 
                user_accepted=True)
        else:
            # здесь, user_accepted = False, потому что второй юзер пока не принял запрос, скипаем этого юзера и больше не показываем в homepage
            match_established = Match.objects.get_or_create(
                current_user=self.request.user, 
                user_requested=partner, 
                user_accepted=False)

            print(match_established)

class UserMatchesListView(LoginRequiredMixin, ListView):
    model = Match
    template_name = 'test/matches.html'
    context_object_name = 'matches'

    def get(self, request, *args, **kwargs):
        self.object_list = self.user_matches(self, request)
        return super().get(request, *args, **kwargs)    

    def user_matches(self, request, *args, **kwargs):
        you_liked_them = Match.objects.filter(
            current_user=self.request.user, 
            user_accepted=True
            ).values_list('user_requested', flat=True)

        they_liked_you = Match.objects.filter(
            current_user__in=you_liked_them, 
            user_accepted=True
            ).values_list('current_user', flat=True).exclude(current_user=self.request.user)

        mutual_like_match_ids = set(you_liked_them).intersection(set(they_liked_you))
        matches = Match.objects.filter(
            current_user=self.request.user, 
            user_requested__in=mutual_like_match_ids
            ).values_list('user_requested')
    
        print(f'mutual match: {matches.all()}')        
        return matches
        
# API

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserAccessPermission]

    @action(detail=False, url_path='login', methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = auth.authenticate(
            username=serializer.validated_data.get('username'),
            password=serializer.validated_data.get('password')
            )
            auth.login(request, user)
            return Response(user, {"Success, you are logged in!"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
 
    @action(detail=False, url_path='logout', methods=['POST'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated, ProfileAccessPermission]
    
    def get_queryset(self):
        accepted_matches = Match.objects.filter(
            current_user=self.request.user, 
            user_accepted=True
            ).values_list('user_requested', flat=True).distinct()

        if accepted_matches:
            return Profile.objects.filter(user__in=accepted_matches)
        return Profile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileSerializerRestricted
        return ProfileSerializer
        

class PreferenceViewsSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    permission_classes = [permissions.IsAuthenticated, PreferenceAccessPermission]

    def get_queryset(self):
        accepted_matches = Match.objects.filter(
            current_user=self.request.user, 
            user_accepted=True).values_list('user_requested', flat=True).distinct()
        if accepted_matches:
            return Preference.objects.filter(user__in=accepted_matches)
        return [{}]

class InterestViewsSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated, InterestAccessPermission]

class MatchViewsSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated, MatchAccessPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(current_user=self.request.user)