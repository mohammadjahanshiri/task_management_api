from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , viewsets , permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet , ViewSet
from .models import *
from .serializers import *
from django.db.models import Q

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all().prefetch_related("tasks")
    serializer_class = ProjectSerializers

    def get_permissions(self):
        if self.action in ["list" , "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Project.objects.all().prefetch_related("tasks")
        return Project.objects.filter(
            Q(owner=user | Q(members=user))
        ).distinct().prefetch_related("tasks")

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

    def get_permissions(self):
        if self.action in ["list" , "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Task.objects.all().select_related("project")
        return Task.objects.filter(
            Q(project__owner=user) | Q(project__members=user)
        ).distinct().select_related("project ")
        
    
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return Comment.objects.filter(task_id=task_id)
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user ,
            task_id=self.kwargs.get("task_id")
        )

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            qs = Activity.objects.all()
        else:
            qs = Activity.objects.filter(
                Q(project__owner=user) |
                Q(project__members=user)
            ).select_related("project" ,"task" , "user").distinct().order_by("-timestamp")