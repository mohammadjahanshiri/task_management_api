from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.utils import timezone

class TaskSerializers(serializers.ModelSerializer):
    
    project_name = serializers.CharField(source="project.title" , read_only=True)

    class Meta:
        model = Task
        fields = ("id","title" , "description" ,"project","project_name" ,"status" , "assigned_to" , "due_date" , "created_at","completed_at" , "updated_at" )
        read_only_fields = ["created_at" , "completed_at" , "updated_at"]

    def validate(self, attrs):
        project = attrs.get("project") or getattr(self.instance , "project" , None)
        assigned_to = attrs.get("assigned_to") or getattr(self.instance , "assigned_to" , None)

        if project and assigned_to:
            if not project.members.filter(pk=assigned_to.pk).exists():
                raise serializers.ValidationError(
                    {"assigned_to" : "This user is not in this project."}
                )
    


        if self.instance:
            old_status = self.instance.status
            new_status = attrs.get('status')

            if new_status and old_status != new_status:

                allowed_transitions = {
                    'UNDONE' :['PROCCESSING'],
                    "PROCCESSING" : ['DONE' , 'UNDONE'],
                    'DONE' : ['PROCCESSING']
                }

                if new_status not in allowed_transitions.get(old_status, []):
                    raise serializers.ValidationError(
                        f"It isn't possible to change {old_status} to {new_status}"
                    )
        return attrs

class ProjectSerializers(serializers.ModelSerializer):
    tasks = TaskSerializers(many=True , read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all() , many=True)

    class Meta:
        model = Project
        fields = ("id" ,"title" ,"description" , "tasks" ,"owner" , "created_at" , "members")
        read_only_fields = ["owner","created_at"]

class CommentSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id","content","author","task","created_at")
        read_only_fields = ["author","task","created_at"]


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = ["id" , "project" , "task" , "user" , "action" , "timestamp"]
        read_only_fields = fields