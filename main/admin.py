from django.contrib import admin
from .models import CustomUser, Bus, Record

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Bus)
admin.site.register(Record)
