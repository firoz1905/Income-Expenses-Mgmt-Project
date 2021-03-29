from . import views
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.urls import path

urlpatterns = [
    path('',views.index,name="preferences"),
    path('account',views.accountPage,name="account"),
    path('account-update',views.account_update,name="account_update"),
    
]
