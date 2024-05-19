from django.contrib import admin
from . models import *

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
