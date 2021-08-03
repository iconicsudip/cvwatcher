from django.contrib import admin
from ats.models import skill,Resume
# Register your models here.
admin.site.register(skill)
@admin.register(Resume)
class resultadmin(admin.ModelAdmin):
    list_display = ['user','resume']