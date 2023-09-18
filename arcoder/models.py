from querybook.models import Solutions
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from program.models import Program
from django.urls import reverse



# getting the user path
def user_image_path(instance, filename):
    return f'files/image/user/{instance.user.username}/{filename}'



# Create your models here.

class Language(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50, primary_key=True)
    category = models.CharField(max_length=500, default='')
    # alphaname = models.CharField(max_length=50, default='')
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.ImageField(upload_to='files/images/languages', default='')
    about = RichTextUploadingField()
    # url_name = models.CharField(max_length=50, blank=True, default='', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("language", kwargs={"lang": self.name})


class user_detail(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, blank=True)
    dob = models.CharField(blank=True,  max_length=10)
    about = models.CharField(blank=True, max_length=300,
                             default='NO DESCRIPTION ADDED')
    image = models.ImageField(upload_to=user_image_path, default='user.png')
    otp = models.CharField(default='150302', max_length=6)
    url_otp = models.CharField(blank=True, max_length=10)
    profile_created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    otp_created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    privacy = models.BooleanField(default=True)

    def program_rating(self):
        count = 0
        pr = Program.objects.filter(author=self.user)
        total = 0
        for i in pr:
            count += 1
            total = total + int(i.total_rating()[0])
        if count == 0:
            count = 1
        return int(total/count)

    def solution_rating(self):
        count = Solutions.objects.filter(author=self.user).count()
        pr = Solutions.objects.filter(author=self.user)
        total = 0
        for i in pr:
            total = total + int(i.total_rating()[0])
        if count == 0:
            count = 1
        return int(total/count)

    def __str__(self):
        return self.user.username
