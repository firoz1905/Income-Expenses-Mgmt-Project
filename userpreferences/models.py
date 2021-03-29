from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here. This is for storing the user preferenes 
class UserPreference(models.Model):
    user=models.OneToOneField (to=User,null=True,on_delete=models.CASCADE) ## Each user has one set of preferences
    currency=models.CharField(max_length=255,blank=True,null=True) ## user when registered will not have anything 
    profile_pic= models.ImageField(default="Profile_Pic_1.png",null=True,blank=True)
    phone = models.CharField(max_length=200,null= True,blank= True)
    dob=models.DateField(null=True,blank=True,default=now)

    def __str__(self):
        return str(self.user)+'s' + 'preferences'

    
