from django.db import models
from django.contrib.auth.models import User


class Grade(models.Model):
    grade = models.CharField(max_length=20)

    def __unicode__(self):
        return self.grade


class Notification(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey(Grade)
    file = models.FileField(upload_to='files/%Y/%m/%d')

    def __unicode__(self):
        return self.title