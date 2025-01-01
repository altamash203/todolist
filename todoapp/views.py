from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Tasks,User
from rest_framework.permissions import IsAuthenticated, AllowAny


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        data =request.data

        serialized_signup = SignUpSerializer(data=data)
        if not serialized_signup.is_valid():
            return Response({"error":serialized_signup.errors},status=status.HTTP_400_BAD_REQUEST)
        serialized_signup.save()

        return Response({"message":"User created successfully", "data":serialized_signup.data},status=status.HTTP_201_CREATED)
class Login(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
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

            else:
                return Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
class Task(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request):
        tasks = Tasks.objects.filter(user=request.user)
        serialized_task = TaskSerializer(tasks,many=True)
        return Response(serialized_task.data,status=status.HTTP_200_OK)
    def post(self,request):
        serialized_task = TaskSerializer(data =request.data)
        if serialized_task.is_valid():
            serialized_task.save()
            return Response(serialized_task.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_task.errors,status=status.HTTP_400_BAD_REQUEST)
class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            task = Tasks.objects.get(user=request.user,pk=pk)
            serialized_task = TaskSerializer(task)
            return Response(serialized_task.data,status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:

             task =Tasks.objects.get(user=request.user,pk=pk)
             serialized_update = TaskSerializer(task,data = request.data)
             if serialized_update.is_valid():
                    serialized_update.save()
                    return Response(serialized_update.data,status=status.HTTP_200_OK)
             else:
                    return Response(serialized_update.errors,status=status.HTTP_400_BAD_REQUEST)
        except Tasks.DoesNotExist:
            return Response({"error":"task not found"},status=status.HTTP_404)

    def delete(self,request,pk):
        try:
            task =Tasks.objects.get(user=request.user,pk=pk)
            task.delete()
            return Response({"message":"task deleted"},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error":"task not found"},status=status.HTTP_404_NOT_FOUND)
class FilterTasks(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):

        filter_status = request.query_params.get('status')
        filter_tag =request.query_params.get('tag')
        tasks = Tasks.objects.all()
        if filter_status:
            tasks = tasks.filter(status=filter_status)
        if filter_tag:
            tasks = tasks.filter(tag__title=filter_tag)

        if not tasks.exists():
            return Response({"error": "No tasks found "}, status=status.HTTP_404_NOT_FOUND)

        serialized_tasks = TaskSerializer(tasks,many=True)
        return Response(serialized_tasks.data,status=status.HTTP_200_OK)









