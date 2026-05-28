from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Activity)
