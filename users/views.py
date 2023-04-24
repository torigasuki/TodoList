from .models import User
from .serializers import UserSerializer, TokenLoginSerializer

from rest_framework import status , permissions

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView

class SignupView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입이 완료되었습니다'},status=status.HTTP_201_CREATED)
        else :
            return Response({'message':f'${serializer.errors}'},status=status.HTTP_400_BAD_REQUEST)
        
        
class TokenLoginView(TokenObtainPairView):
    serializer_class = TokenLoginSerializer
    
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        user =get_object_or_404(User,id=id)
        serialize = UserSerializer(user)
        return Response(serialize.data)
    
    def put(self, request, id):
        user = get_object_or_404(User,id=id)
        if request.user == user:
            serialize = UserSerializer(user,data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data)
            else:
                return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({'message':'권한이 없습니다.'}, status = status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, id):
        user = get_object_or_404(User,id=id)
        if request.user == user:
            user.delete()
            return Response({'message':'삭제되었습니다.'})