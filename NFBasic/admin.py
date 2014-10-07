from django.contrib import admin
from NFBasic.models import *


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'content', 'created_time', 'show_admin_thumb')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_time'
    list_filter = ('grade', 'month', 'created_time')

admin.site.register(Notification, NotificationAdmin)