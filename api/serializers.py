from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils import field_mapping
from datum.models import User, Profile, Preference, Interest, Match

class UserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        models = Profile
        fields = '__all__'

