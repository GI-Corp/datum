from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils import field_mapping
from datum.models import User, Profile, Preference, Interest, Match

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password',)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        fields = ('username', 'password',)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, validated_data):
        raise NotImplementedError


class ProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileSerializerRestricted(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'tg_username', 'first_name', 'last_name')

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

