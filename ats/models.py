from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class skill(models.Model):
    skill = models.TextField(max_length=100,blank=True,default=None)
    catagory = models.TextField(max_length=100,blank=True,default=None)
    
    def __str__(self):
        return self.skill
    
class Resume(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resume = models.FileField(upload_to="",default="")

    