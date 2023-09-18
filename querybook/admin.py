from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Query)
admin.site.register(Solutions)
admin.site.register(query_form)
admin.site.register(solution_form)
admin.site.register(solution_rating)
