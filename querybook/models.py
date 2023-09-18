from typing import Tuple
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse



class Query(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=500)
    description = RichTextUploadingField(blank=True)
    language = models.CharField(max_length=50)
    slug = models.CharField(max_length=300, default="", blank=True)
    answer = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    time_stamp = models.DateField(auto_now_add=True, blank=True)
    prism_name = models.CharField(max_length=50, blank = True)
    keyword = models.CharField(max_length=500, blank = True, null=True)



    class Meta:
        ordering = ['-id']


    def __str__(self):
        return self.query + " " + self.language

    def get_absolute_url(self):
        return reverse("final_query", kwargs={"language": self.language, 'query_slug': self.slug})


class Solutions(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE , null=True)
    solution = RichTextUploadingField()
    like = models.ManyToManyField(User, related_name='solution_like', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateField(auto_now_add=True, blank=True)
    url = models.URLField(max_length=200, blank=True)



    class Meta:
        ordering = ['-id']

    
    def likeCount(self):
        return self.like.count()

    def total_rating(self):
        count = solution_rating.objects.filter(solution=self).count()
        pr = solution_rating.objects.filter(solution=self)
        total = 0
        for i in pr:
            total += i.rating
        if count == 0:
            return [int(total * 20)/1, count, total]
        return [int(total * 20)/count, count, total]


    def __str__(self):
        return self.query.query + " " + self.query.language +" "+self.author.username 



# solution rating
class solution_rating(models.Model):
    solution = models.ForeignKey(Solutions, on_delete = models.CASCADE)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    rating = models.FloatField(blank = True)
    def __str__(self):
        return self.solution.query.query + " " + self.user.username + ' ' + str(self.rating)




class query_form(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.CharField(max_length= 255)
    description =RichTextUploadingField(blank = True, null = True)

    def __str__(self):
        return self.title
    

class solution_form(models.Model):
    id = models.AutoField(primary_key=True)
    solution = RichTextField()



# slug classes
def create_slug(instance, new_slug=None):
    temp = instance.query
    language = instance.language

    slug_list = temp.split(" ")
    separator = "-"
    temp_slug = separator.join(slug_list)
    slug_list = temp_slug.split('/')
    temp = '_'.join(slug_list)

    slug = slugify(temp)
    return slug


def pre_save_program(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_program, sender=Query)



# def create_slug(instance, new_slug=None):
#     temp = instance.title
#     language = instance.language

#     slug_list = temp.split(" ")
#     separator = "-"
#     temp_slug = separator.join(slug_list)
#     slug_list = temp_slug.split('/')
#     temp = '_'.join(slug_list)

#     slug = slugify(temp)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Query.objects.filter(query=slug, language = language).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug
