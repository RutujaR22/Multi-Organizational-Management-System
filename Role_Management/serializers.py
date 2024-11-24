from rest_framework import serializers
from .models import Organization, User

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name"]

    def validate(self, data):
        user = self.context.get('request').user
        if not (user.is_superuser or (user.organization.is_main and user.role.name == "Admin")):
            raise serializers.ValidationError("You do not have permission to manage organizations.")
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = ["id", "username", "organization", "role"]
    
    def validate(self, data):
        user = self.context.get('request').user
        if not (user.role.name == "Admin"):
            raise serializers.ValidationError("You do not have permission to manage organization.")
        return data
