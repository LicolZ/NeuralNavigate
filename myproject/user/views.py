### views.py - handle HTTP requests and responses ###

# Django imports
import os
import datetime
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Third-party imports
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from user.models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


# Local imports
from scripts.extract_topics import ProcessFile
from user.serializers import UserSerializer

def generate_token_for_user(user):
    """Generate JWT token for a user."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class SignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        print("Inside SignupView post method")  # Add this
        # # Extract email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if either email or password is missing
        if not email or not password:
            return JsonResponse({"non_field_errors": ["Missing required fields"]}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
        
            serializer.save()
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            token = generate_token_for_user(user)
            return JsonResponse({
                'response': 'Successfully registered a new user.',
                'email': user.email,
                'token': token
            }, status=status.HTTP_201_CREATED)
        
        
        print("Serializer Errors:", serializer.errors)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not password:
            return JsonResponse({"non_field_errors": ["Missing required fields"]}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user:
            user.last_login = datetime.datetime.now()
            user.save()
            token = generate_token_for_user(user)
            return JsonResponse({"token": token}, status=status.HTTP_200_OK)
        
        return JsonResponse({"non_field_errors": ["Invalid login credentials"]}, status=status.HTTP_401_UNAUTHORIZED)


class ProcessFileView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        file = request.data.get('file')
        if file:
            file_path = default_storage.save('temp.pdf', file)
            process_file = ProcessFile(file_path)
            topics = process_file.extract_topics()
            relationships = process_file.fetch_topic_relationships(topics)
            return JsonResponse({"topics": topics, "relationships": relationships})
        
        return JsonResponse({'error': 'No file provided'}, status=400)

# class HealthCheckFileView(APIView):
#     parser_class = (FileUploadParser)

#     def post(self, request, *args, **kwargs):
#         print("hello world version 1.0!")

#         return JsonResponse({"hello": "world"})
        