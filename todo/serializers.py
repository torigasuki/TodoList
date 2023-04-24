from .models import Todo

from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
        
    class Meta:
        model = Todo 
        fields = ['title','content','is_done','user']

class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo 
        fields = ['title','content','is_done']
        