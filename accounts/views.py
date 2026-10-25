from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import RegisterSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)