from django.urls.base import reverse
from querybook.models import Query
from django.contrib.sitemaps import Sitemap
from program.models import program_title
from querybook.models import Query
from .models import Language

class program_sitemap(Sitemap):
    changefreq = 'hourly'
    priority = 1

    def items(self):
        return program_title.objects.all()


class query_sitemap(Sitemap):
    changefreq = 'hourly'
    priority = 1

    def items(self):
        return Query.objects.all()


class language_sitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Language.objects.all()


class home_static_sitemaps(Sitemap):
    def items(self):
        return ['home']
    
    def location(self, item):
        return reverse(item)
