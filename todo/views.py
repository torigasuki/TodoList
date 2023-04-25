from .models import Todo
from .serializers import TodoSerializer,TodoCreateSerializer
from django.utils import timezone
import pytz
from rest_framework import status , permissions

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView


class TodoView(APIView):
    def get(self,request):
        todos = Todo.objects.all()
        serialize = TodoSerializer(todos, many=True)
        return Response(serialize.data)
    
    def post(self,requset):
        if not requset.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED) 
        serializer = TodoCreateSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save(user = requset.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class TodoDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,id):
        todo = get_object_or_404(Todo,id=id)
        serialize = TodoSerializer(todo)
        return Response(serialize.data)
    
    
    def put(self,request,id):
        todo = get_object_or_404(Todo,id=id)
        if request.user == todo.user:
            serializer = TodoCreateSerializer(todo,data=request.data)
            if serializer.is_valid():
                if request.data.get('is_done') == True:
                    local_tz = timezone.get_current_timezone()
                    utc_now = timezone.now().astimezone(pytz.utc)
                    local_now = utc_now.astimezone(local_tz)
                    serializer.save(completion_at = local_now)
                else:
                    serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'권한이 없습니다'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request,id):
        todo = get_object_or_404(Todo,id=id)
        if request.user == todo.user:
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'권한이 없습니다'},status=status.HTTP_401_UNAUTHORIZED)