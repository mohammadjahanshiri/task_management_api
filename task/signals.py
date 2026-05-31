from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


# @receiver(post_save , sender=Task)
# def log_task_activity(sender,instance,created,**kwargs):
#     if created:
#         action_text = f"task '{instance.title}'created."
#     else:
#         action_text = f"task '{instance.title}'updated."

#     owner = instance.project.owner

#     if hasattr(owner , 'all'):
#         owner = owner.first()

#     assigned_user = instance.assigned_to.first()
#     user_to_log = assigned_user or instance.project.owner


#     Activity.objects.create(
#         project=instance.project,
#         user=user_to_log,
#         task=instance,
#         action=action_text
#     )


@receiver(post_save , sender=Comment)
def log_comment_activity(sender,instance,created,**kwargs):
    if created:
        Activity.objects.create(
            project=instance.task.project,
            user=instance.author,
            task=instance.task,
            action= f"on '{instance.task.title}'task commented: '{instance.content[:30]}...'"
        )