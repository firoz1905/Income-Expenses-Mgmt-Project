from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    amount=models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    category=models.CharField(max_length=256) ## present use with predefined categories
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE) ## one user can add many expense. 

    def __str__(self):
        return self.category
    
    class Meta: ## latest expenses will be shown first 
        ordering: ['-date']
    
class Category(models.Model):
    name=models.CharField(max_length=255)

    class Meta: ### how this model be called in a plural form . Reason for this is in admin site , i see class name as categorys (prefixed with s)
        ## below will define how this model should be called in plural form
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name