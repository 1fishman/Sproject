from django.contrib import admin
from .models import Student,Score,Class
# Register your models here.
admin.site.register(Score)
admin.site.register(Student)
admin.site.register(Class)