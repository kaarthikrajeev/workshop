from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Registration)
admin.site.register(Technician)
admin.site.register(Schedule)
admin.site.register(Request)
admin.site.register(Feedback)