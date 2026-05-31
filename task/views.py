from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , viewsets , permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet , ViewSet
from .models import *
from .serializers import *
from django.db.models import Q
from .filters import TaskFilter

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
    filterset_class = TaskFilter
    ordering_fields = ['created_at','status']
    ordering = ['-created_at']

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
    
    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status

        task = serializer.save()
        new_status = task.status

        if old_status != new_status:
            if new_status == 'DONE':
                task.completed_at = timezone.now()
            elif old_status == 'DONE':
                task.completed_at = None

            task.save(update_fields=['completed_at'])

            Activity.objects.create(
                project=task.project ,
                user=self.request.user,
                task=task,
                action=f"The position of task changed from {old_status} to {new_status}."
            )
        
    
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