from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email','password','username','gender','age','introduction'] 
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def create(self, validated_data):
        user = super().create(validated_data) 
        password = user.password
        user.set_password(password) 
        user.save()
        return user
    
    def update(self , instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    
    
class TokenLoginSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['gender'] = user.gender
        token['age'] = user.age
        return token
