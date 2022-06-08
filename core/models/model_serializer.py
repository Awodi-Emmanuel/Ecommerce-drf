from dataclasses import field
from typing import Union


from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, IntegerField, ListSerializer
from rest_framework.serializers import ModelSerializer as DrfModelSerializer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework_simplejwt.tokens import RefreshToken

from core.models.implementation import(
    Category,
    Product,
) 

User = get_user_model()

class MyListSerializer(ListSerializer):
    @property
    def data(self):
        ret = super().data
        return ReturnList(ret, serializer=self)
    
class ModelSerializer(DrfModelSerializer):
    class Meta:
        list_serializer_class = MyListSerializer  
        
        
class PublicUserSerializer(ModelSerializer):
    id = IntegerField()
    username = CharField(required=False) 
    
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "is_active") 
        
class UserSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "email_is_verified"
        )
        
        def get_tokens(self, instance: User) -> Union[dict, None]:
            refresh = RefreshToken.for_user(instance)
        
            # print('refresh: ' + str(refresh))
            # print('access_token: ' + str(refresh.access_token))
            
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }                 

class CategorySerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent_category_id",
            "slug",
            "created_at",
            "updated_at"
        )   

class ProductSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model =  Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "available",
            "date_added",
            "updated"
        )
        