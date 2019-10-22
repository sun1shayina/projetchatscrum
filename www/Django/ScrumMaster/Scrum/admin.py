from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ScrumUser)
admin.site.register(ScrumGoal)
admin.site.register(ScrumProject)
admin.site.register(ScrumProjectRole)
admin.site.register(ScrumDemoProject)
admin.site.register(ScrumChatRoom)
admin.site.register(ScrumChatMessage)
admin.site.register(ScrumSprint)