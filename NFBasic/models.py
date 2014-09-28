from django.db import models
from django.contrib.auth.models import User


class Grade(models.Model):
    grade = models.CharField(max_length=20)

    def __unicode__(self):
        return self.grade


class NotificationMonth(models.Model):
    month = models.DateTimeField()

    def __unicode__(self):
        return self.month.strftime("%Y-%m")


class Notification(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey(Grade)
    month = models.ForeignKey(NotificationMonth)
    file = models.FileField(upload_to='files/%Y/%m/%d', blank=True)

    def __unicode__(self):
        return self.title

    def image(self):
        if self.file:
            return '<a href="%s"><img width="50" height="50" src="%s" /></a>' % (self.file.url, self.file.url)
        else:
            return 'No Images'
    image.allow_tags = True