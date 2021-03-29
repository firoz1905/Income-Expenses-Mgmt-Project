from django.contrib import admin
from .models import Expense,Category



class ExpensesAdmin(admin.ModelAdmin):
    list_display=('amount','description','owner','category','date',)
    search_fields=('description','category','date','amount',)
    list_per_page=7

## note : We can create a super user to our website  - python manage.py createsuperuser
## or Login python shell and perfomr the below command 
 ### User.objects.create_superuser(u'username', u'email', u'password')

 # Register your models here.
admin.site.register(Expense,ExpensesAdmin)
admin.site.register(Category)