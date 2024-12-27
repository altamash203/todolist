from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

class Tasks(models.Model):
    priority_choices =[('Optional','Optional'),
                       ('Medium','Medium'),
                       ('Necessary','Necessary'),
                       ("Urgent","Urgent"),
                       ("Critical","Critical")
                       ]
    id=models.AutoField(primary_key= True)
    title=models.CharField(max_length=20)
    description =models.TextField()
    tag =models.ManyToManyField("Tag",related_name="tasks")
    dead_line =models.DateTimeField()
    priority =models.CharField(max_length=10,choices=priority_choices)
    user =models.ForeignKey("User",on_delete=models.CASCADE,related_name="tasks",null = False)


    def __str__(self):
        return self.title

class Tag(models.Model):
    id =models.AutoField(primary_key=True)
    title = models.CharField(max_length=25)


    def __str__(self):
        return self.title










