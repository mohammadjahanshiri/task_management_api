import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='exact')
    project = django_filters.NumberFilter(field_name='project')
    assigned_to = django_filters.NumberFilter(field_name='assigned_to')

    class Meta:
        model = Task
        fields = ['title' , 'status' , 'project' , "assigned_to"]