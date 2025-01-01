from django.urls import path
from . import views


urlpatterns= [
     path("signup/",views.SignUp.as_view()),
     path("login/",views.Login.as_view()),
     path("tasks/all_tasks/",views.Task.as_view()),
     path("tasks/add_task/", views.Task.as_view()),
     path("tasks/<int:pk>/",views.TaskDetail.as_view()),
     path("tasks/filter/", views.FilterTasks.as_view()),


]
