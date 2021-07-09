from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.forms import ModelForm

from DatumApp.models import Interest, Match, Preference, Profile


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['interest_title']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'first_name', 'last_name', 'tg_username', 'registered_date', 'last_update_date',)


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        exclude = ('user',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self):
        user: User = super().save(commit=True)
        user.set_password(user.password)
        user.save()
        return user
    

class UserLoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']