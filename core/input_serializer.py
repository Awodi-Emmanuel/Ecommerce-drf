from datetime import datetime, timedelta
from xml.dom import ValidationErr

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import validate_email as dj_validate_email
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.fields import *
from rest_framework.serializers import Serializer, ValidationError

from core.models import TempCode
User = get_user_model()

class SignupInputSerializer(Serializer):
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    email = EmailField()
    phone = CharField()
    password = CharField()
    
    class Meta:
        ref_name  = None
        
    def validate_username(self, *args):
        username = self.initial_data["username"]
        u = User.objects.filter(username=username).first()
        if u:
         #and u.date_joined >= datetime(2020, 1, 1, tzinfo=pytz.UTC):
            raise ValidationErr("This username is already used.")
        return username
    
    def validate_email(self, *args):
        email = self.initial_data["email"]
        try:
            dj_validate_email(email)
            user = User.objects.filter(email=email).first()
            if user:
                raise ValidationErr("This email is already used.")
        except ValidationErr as e:
            raise e
        
        return email
    
    def create_user(self):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        phone = self.validated_data["phone"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        password = self.validated_data["password"]
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            user = User.objects.create_user(
                username=username,
                email=email,
                phone_number=phone,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            user.is_active = False
            user.save()
            
        else:
            raise ValidationErr("User already exist")
        
        return user
    
    
class SigninInputSerializer(Serializer):
    email = EmailField(required=False, allow_null=True)
    username = CharField(required=False, allow_null=True)
    password = CharField
    
    class Meta:
        ref_name = None
        
    def validate_password(self, *args):
        email = self.initial_data.get("email")
        username = self.initial_data.get("username")
        password =  self.initial_data.get("password")
        
        if not email and not username:
            raise ValidationError(_("(username or email) fields should be present."))
        
        return password
    
class ConfirmInputSerializer(Serializer):
    email = EmailField()
    code = CharField()
      
    class Meta:
        ref_name = None  
        
class  ValidateOTPInputSerializer(Serializer):
    email = EmailField()
    otp = CharField()
    
    class Meta:
        ref_name = None        
            