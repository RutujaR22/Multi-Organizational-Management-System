from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        if not username:
            raise ValueError("Username is required.")

        from Role_Management.models import User
        user = User(username = username, email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, password = None, role = None, **extra_fields):             # Creating superuser/django-admin in django
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        from Role_Management.models import Organization
        main_org = Organization.objects.filter(is_main = True).first()

        if not main_org:
            raise ValueError("Main organization doesn't exists. Please create one first.")
        extra_fields['organization'] = main_org
        
        if role is None:
            from Role_Management.models import Role
            role = Role.objects.get(name = "Admin")
        
        user = self.create_user(username, email, password, role = role, **extra_fields)
        Token.objects.get_or_create(user = user)
        return user