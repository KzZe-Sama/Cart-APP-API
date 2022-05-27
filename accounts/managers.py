from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, address,phone,password=None ):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email),address=address,phone=phone)
        user.set_password(password)
        user.save()

        return user
    def create_superuser(self, username, email, password,phone,address):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username=username, email=email, password=password,phone=phone,address=address)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user