from distutils.log import error
from email.policy import default
import imp
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from user.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
import json



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username','fullname', 'email', 'password']
        extra_kwargs = {
            'password':{'write_only': True}
        }


    def validate(self, attrs):
        username = attrs.get('username')
        fullname = attrs.get('fullname') 
        email = attrs.get('email')
        password = attrs.get('password')

        if username and password and fullname and email:
            if User.objects.filter(username=username).exists():
                msg = _('A user with this username exists')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('User info is not valid')

        return attrs

    def save(self):
        user= User(
            email = self.validated_data['email'],
            fullname = self.validated_data['fullname'],
            username = self.validated_data['username'],
        
        ) 
        
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
            
        return user


class LoginSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password') 

        if username and password:
            try:
                user = authenticate(request=self.context.get('request'),
                        username=username, password=password)

                if not user:
                    msg = _('Username or password is incorrect.')
                    raise serializers.ValidationError(msg, code='authorization')
            except User.DoesNotExist:
                msg = _('Username or password is incorrect or is not registered yet.')
                raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
