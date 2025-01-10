from django.urls import path
from . import views


urlpatterns= [
     path("signup/",views.SignUp.as_view()),
     path("login/",views.Login.as_view()),
     path("tasks/",views.TaskList.as_view()),
     path("task/<int:pk>/",views.Task.as_view()),
     path("task/",views.Task.as_view())

]
