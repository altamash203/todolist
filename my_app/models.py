from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tasks(models.Model):
    priority_choices =[('Optional','Optional'),
                       ('Medium','Medium'),('Necessary','Necessary'),
                       ("Urgent","Urgent"),
                       ("Critical","Critical")
                       ]
    task_id=models.AutoField(primary_key= True)
    title=models.CharField(max_length=20)
    description =models.TextField()
    tag =models.ManyToManyField("Tag",related_name="tasks")
    dead_line =models.DateTimeField()
    priority =models.CharField(max_length=10,choices=priority_choices)
    user_id =models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Tag(models.Model):
    tag_id =models.AutoField(primary_key=True)
    tag_title = models.CharField(max_length=25)


    def __str__(self):
        return self.tag_title


