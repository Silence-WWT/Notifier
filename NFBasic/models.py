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


class NotificationImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    length = models.CharField(max_length=20)
    md5 = models.CharField(max_length=40)
    view_thumb = models.ImageField(upload_to='images/%Y/%m/%d')
    admin_thumb = models.ImageField(upload_to='images/%Y/%m/%d')

    def __unicode__(self):
        return self.image.name


class NotificationFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')
    length = models.CharField(max_length=20)
    md5 = models.CharField(max_length=40)
    image = models.OneToOneField(NotificationImage, blank=True, null=True)

    def __unicode__(self):
        return self.file.name


class Notification(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey(Grade)
    month = models.ForeignKey(NotificationMonth)
    images = models.ManyToManyField(NotificationImage, blank=True, null=True)
    files = models.ManyToManyField(NotificationFile, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def show_image(self):
        if self.image:
            return '<a href="%s"><img src="%s" /></a>' % (self.image.url, self.image.url)
        else:
            return 'No Images'
    show_image.allow_tags = True

    def show_admin_thumb(self):
        images = []
        for image in self.images.all():
            images.append('<a href="%s"><img src="%s" /></a>' % (image.admin_thumb.url, image.admin_thumb.url))
        if images:
            return images
        else:
            return 'No images'
    show_admin_thumb.allow_tags = True