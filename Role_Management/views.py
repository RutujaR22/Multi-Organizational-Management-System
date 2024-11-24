from django.shortcuts import render
from rest_framework.views import APIView
from .models import Organization, User, Role
from .serializers import OrganizationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.

# Organization CRUD Operations (To allow the main organization’s admin to create, update, and delete sub-organizations.)
class OrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):                             # To get all organization                        
        try:
            organizations = Organization.objects.all()
            serializer = OrganizationSerializer(organizations, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):                                 # To create organization
        try:
            data = request.data
            serializer = OrganizationSerializer(data = data, context = {'request': request})
            if serializer.is_valid():     
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors) 
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request):                          # To update organization
        try:
            data = request.data
            obj = Organization.objects.get(id = data.get("id"))
            serializer = OrganizationSerializer(obj, data = data, partial = True, context = {'request': request})
            if serializer.is_valid():     
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):                         # To delete organization
        try:
            data = request.data
            obj = Organization.objects.get(id = data.get("id"))
            obj.delete()
            return Response({'message': 'Organization deleted'})
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)


# User CRUD operations(To allow admins to create, view, update, and delete users within their own organization.)
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):                        # To get all users of organization
        try:
            users = User.objects.filter(organization = request.user.organization)      # Getting users of organization which admin belongs to
            serializer = UserSerializer(users, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):                   # To create user of same organization as admin
        try:
            data = request.data
            serializer = UserSerializer(data = data, context = {'request': request})
            if serializer.is_valid():
                serializer.save(organization = request.user.organization)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request):                          # To update user of organization
        try:
            data = request.data
            obj = User.objects.get(id = data.get("id"))
            if obj.organization != request.user.organization:
                return Response({"message": "You cannot update users from other organization."})
            serializer = UserSerializer(obj, data = data, partial = True, context = {'request': request})
            if serializer.is_valid():     
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
  
    def delete(self, request):                    # To delete user
        try:
            data = request.data
            obj = User.objects.get(id = data.get("id"))
            if obj.organization != request.user.organization:
                return Response({"message": "You cannot delete users from other organization."})
            obj.delete()
            return Response({'message': 'User deleted'})
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)


# API to assign roles to users
class RoleAssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            if not request.user.role.name == "Admin":
                return Response({"message": "Unauthorized."})

            obj = User.objects.get(id = request.data.get("user_id"))
            if obj.organization != request.user.organization:
                return Response({"message": "You cannot assign roles to users from other organization."})
        
            role = Role.objects.get(id = request.data.get("role_id"))
            obj.role = role
            obj.save()
            return Response({'message': 'Role assigned'})
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)


# API for user login
class LoginAPI(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username = username, password = password)
            if not user:
                return Response({"message": "Invalid credentials"})
            Token.objects.get_or_create(user = user)
            return Response({
                "username": user.username,
                "organization": user.organization.name if user.organization else None,
                "role": user.role.name if user.role else None,
            })
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
