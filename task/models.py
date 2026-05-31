from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    owner = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank=True , related_name='projects')
    members = models.ManyToManyField(User , related_name='joined_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField()
    description = models.CharField()
    project = models.ForeignKey(Project , on_delete=models.CASCADE , related_name='tasks')
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL ,null=True , related_name='tasks')
    STATUS = [
        ('DONE' , 'DONE') , ('PROCCESSING', 'PROCCESSING') , ('UNDONE' , 'UNDONE')
    ]
    status = models.CharField(max_length=12 , choices=STATUS , default='PROCCESSING')
    due_date = models.DateTimeField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True , null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task , on_delete=models.CASCADE , related_name='comments')
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    project = models.ForeignKey(Project , on_delete=models.CASCADE , related_name="activities")
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    task = models.ForeignKey(Task , on_delete=models.SET_NULL ,related_name="activities", null=True , blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']