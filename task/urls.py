from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"projects" , ProjectViewSet , basename="project")
router.register(r"tasks" , TaskViewSet , basename="task")
router.register(r"activities" , ActivityViewSet , basename="activity")

comment_list = CommentViewSet.as_view({
    "get" : "list" ,
    "post" : "create"
})

app_name = "task"


urlpatterns = router.urls  + [
    path("tasks/<int:task_id>/comments/" , comment_list , name="task_comments")

]