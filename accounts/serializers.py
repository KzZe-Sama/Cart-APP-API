from django.db.models import fields
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import json
import datetime
from json import JSONEncoder

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    class Meta:
        model = User
        fields = ['email', 'username', 'password','address','phone']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    class Meta:
        model = User
        fields = ('id','email', 'username', 'password','address','phone','date_joined','is_staff','is_superuser')


    def update(self, instance, validated_data):
    #    Updating User Details
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    
    def get_token(cls, user):
        token = super().get_token(user)
        
        # print(token)
        return token
class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'username','address','phone','date_joined','is_staff','is_superuser')
    # def validate(self, attr):
    #     data = super().validate(attr)
    #     data['username'] = self.user.username
    #     data['email'] = self.user.email
    #     data['phone'] = self.user.phone
    #     data['address'] = self.user.address
    #     data['date_joined'] = json.dumps(self.user.date_joined,indent=4, cls=DateTimeEncoder)
    #     data['is_superuser'] = self.user.is_superuser
    #     data['is_staff'] = self.user.is_staff
    #     return data
