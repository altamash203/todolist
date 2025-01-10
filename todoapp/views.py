from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Tasks
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

class SignUp(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serialized_signup = SignUpSerializer(data=request.data)
        if not serialized_signup.is_valid():
            return Response({"error":serialized_signup.errors},status=status.HTTP_400_BAD_REQUEST)
        serialized_signup.save()
        #direct login after signup
        email =request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email,password=password)
        refresh = RefreshToken.for_user(user)
        return Response({"message":"User created successfully",
                         "refresh":str(refresh),
                         "access":str(refresh.access_token)},
                        status=status.HTTP_201_CREATED)
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return Response({"error":"Please provide all the required fields"},status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(email=email,password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({"refresh":str(refresh),"access":str(refresh.access_token),"message":"login successful"},status=status.HTTP_200_OK)
            elif not  get_user_model().objects.filter(email=email).exists():
                return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
class TaskList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Task_Get_Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status','tag__title']
    def get_queryset(self):
        query_set = Tasks.objects.filter(user=self.request.user)

        return query_set



class Task(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.data["user"] = request.user.id
        serialized_task = Task_Post_Put_Serializer(data=request.data)
        if serialized_task.is_valid():
            serialized_task.save()
            return Response(serialized_task.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_task.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,pk):
        try:
            task = Tasks.objects.get(user=request.user,pk=pk)
            serialized_task = Task_Get_Serializer(task)
            return Response(serialized_task.data,status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:
             task =Tasks.objects.get(user=request.user,pk=pk)
             serialized_update = Task_Post_Put_Serializer(instance=task,data = request.data)
             if serialized_update.is_valid():
                    serialized_update.save()
                    return Response(serialized_update.data,status=status.HTTP_200_OK)
             else:
                    return Response(serialized_update.errors,status=status.HTTP_400_BAD_REQUEST)
        except Tasks.DoesNotExist:
            return Response({"error":"task not found"},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,pk):
        try:
            task =Tasks.objects.get(user=request.user,pk=pk)
            task.delete()
            return Response({"message":"task deleted"},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error":"task not found"},status=status.HTTP_404_NOT_FOUND)


















