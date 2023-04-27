from .models import Todo
import datetime
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
        
    class Meta:
        model = Todo 
        fields = ['id','title','content','is_done','user','completion_at']

class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo 
        fields = ['title','content','is_done']
        
class TodoPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo 
        fields = ['is_done','completion_at']
        
    def update(self, instance, validated_data):
        instance.is_done = validated_data.get('is_done', instance.is_done)
        if instance.is_done==True:
            instance.completion_at = datetime.datetime.now()
        instance.save()
        return instance