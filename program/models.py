from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save
from django.utils.text import slugify
from meta.models import ModelMeta
from django.urls import reverse
import json


# Create your models here.
class program_title(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 255)
    language = models.CharField(max_length=50)
    slug = models.CharField(max_length=300, default="")
    answers = models.IntegerField(default=1)
    prism_name = models.CharField(max_length=50, blank = True)
    keyword = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.title + " " + self.language
        
    def get_absolute_url(self):
        return reverse("final_program", kwargs={"lang": self.language, 'slug': self.slug})
    

    class Meta:
        ordering = ['id']




class Program(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(program_title, on_delete=models.CASCADE , null=True)
    code = RichTextUploadingField()
    # code = models.TextField(default='')
    like = models.ManyToManyField(User, related_name='program_like', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timeStamp = models.DateField(auto_now_add=True, blank=True)
    url = models.CharField(max_length = 200, blank=True, null=True) 




    class Meta:
        ordering = ['id']
        # ordering = ['like_count']


    def like_count(self):
        return self.like.count()

    def total_rating(self):
        count = program_rating.objects.filter(program = self).count()
        pr = program_rating.objects.filter(program = self)
        total = 0
        for i in pr:
            total += i.rating
        if count == 0:
            return [int(total * 20)/1, count, total] 
        return [int(total * 20)/count, count, total] 

    # return the title detail in json form
    def title_detail(self):
        title = self.title.title
        self.title.title = title.replace('\"', '&quot;')
        self.title.title = title.replace('\"', '&apos;')
        

        data = {'title': self.title.title, 
        'answers' : self.title.answers, 
        'language':self.title.language, 
        'slug':self.title.slug,
        'id':self.id}
        
        return data

    def __str__(self):
        return self.title.title + " " + self.title.language 



class program_rating(models.Model):
    program = models.ForeignKey(Program, on_delete = models.CASCADE)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    rating = models.FloatField(blank = True)
    def __str__(self):
        return self.program.title.title + " " + self.user.username + ' ' + str(self.rating)


class form(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=800)
    code = RichTextUploadingField()
    def __str__(self):
        return self.title




# slug classes
def create_slug(instance, new_slug=None):
    temp = instance.title

    slug_list = temp.split(" ")
    separator = "-"
    temp_slug = separator.join(slug_list)
    slug_list = temp_slug.split('/')
    temp = '_'.join(slug_list)

    slug = slugify(temp)
    if new_slug is not None:
        slug = new_slug
    qs = program_title.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_program(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_program, sender=program_title)


