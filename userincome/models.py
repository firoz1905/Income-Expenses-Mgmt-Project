from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class UserIncome(models.Model):
    amount=models.FloatField() ## Decimal Field recommended but i just gone with float
    date=models.DateField(default=now)
    description=models.TextField()
    source=models.CharField(max_length=256) ##source of income
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE) ## one user can add many expense. 

    def __str__(self):
        return self.source
    
    class Meta: ## latest expenses will be shown first 
        ordering: ['-date']
    
class Source(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
