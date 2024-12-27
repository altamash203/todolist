from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Tasks,User
class SignUp(APIView):
    def post(self,request):
        data =request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if not email or not username or not password:
            return Response({"error":"Please provide all the required fields"},status=status.HTTP_400_BAD_REQUEST)

        elif User.objects.filter(email=email).exists():
            return Response({"error":"User with this email already exists"},status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(email=email,username=username,password=password)
            return Response({"message":"User Created Successfully","user":{"email":user.email,"username":user.username}},status=status.HTTP_201_CREATED)

class Login(APIView):
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


class TaskLists(APIView):
    def get(self,request):
        tasks = Tasks.objects.all()
        seriaized_task = TaskSerializer(tasks,many=True)
        return Response(seriaized_task.data,status=status.HTTP_200_OK)

class Task(APIView):

    def post(self,request):
        serialized_task = TaskSerializer(data =request.data)
        if serialized_task.is_valid():
            serialized_task.save()
            return Response(serialized_task.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_task.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        try:
            task = Tasks.objects.get(pk=pk)
            serialized_task = TaskSerializer(task)
            return Response(serialized_task.data,status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:

             task =Tasks.objects.get(pk=pk)
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
            task =Tasks.objects.get(pk=pk)
            task.delete()
            return Response({"message":"task deleted"},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error":"task not found"},status=status.HTTP_404_NOT_FOUND)

class FilterTasks(APIView):

    def get(self,request,status=None,tag=None):

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









