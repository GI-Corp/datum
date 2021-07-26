from os import stat
from re import S
from django.db.models import manager
from django.http import HttpResponse, JsonResponse, Http404, request
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from datum.models import User, Profile, Preference, Interest, Match
from api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]




    