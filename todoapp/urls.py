from django.urls import path
from . import views


urlpatterns= [
     path("signup/",views.SignUp.as_view()),
     path("login/",views.Login.as_view()),
     path("tasks/list/",views.TaskLists.as_view()),
     path("tasks/<int:pk>/",views.Task.as_view()),
     path("tasks/filter/",views.FilterTasks.as_view()),
]
