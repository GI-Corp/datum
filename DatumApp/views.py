from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, SuccessURLAllowedHostsMixin
from django.contrib.messages.api import add_message, success
from django.contrib.messages.context_processors import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models, reset_queries
from django.db.migrations.operations.models import DeleteModel
from django.db.models import fields
from django.db.models.base import Model
from django.forms.models import ModelForm
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse, reverse_lazy
from django.utils.cache import get_max_age
from django.views.generic import CreateView, DetailView
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from urllib3 import fields

from .forms import PreferenceForm, ProfileForm, UserForm, UserLoginForm
from .models import Interest, Match, Preference, Profile

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
                matches = resulting_matches.exclude(user=request.POST.get('user_profile'))
                your_partner = request.POST.get('user_profile')
                self.your_matches(self, request, your_partner, status=False)

        if request.POST.get('Like') == 'Like':
            your_partner = request.POST.get('user_profile')
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
                id=current_user.user_profile.id
                ).values_list('user', flat=True).distinct()

        users_by_age = Profile.objects.filter(
            birthdate__lte=current_user.user_preference.get_min_date(), 
            birthdate__gte=current_user.user_preference.get_max_date()
        ).exclude(id=current_user.user_profile.id).values_list('user', flat=True).distinct()

        resulting_match = set(users_by_interest).intersection(users_by_age)
        
        num_users = len(resulting_match)
        print(f'final matches for {current_user}: {resulting_match}')

        matches = Profile.objects.filter(user__in=resulting_match)
        return matches
        
    def your_matches(self, request, your_partner, status):
        partner = User.objects.get(user=self.your_partner)
        match_exists = Match.objects.filter(current_user=self.request.user, user_requested=partner).exists()
        if not match_exists:
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
        self.object_list = self.userMatches(self, request)
        return super().get(request, *args, **kwargs)    

    def userMatches(self, request, *args, **kwargs):
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