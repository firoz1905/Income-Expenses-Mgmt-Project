from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserPreference
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from django.core.files import File

@login_required(login_url="/authenticationapp/login")
# Create your views here.
def index(request):
    currency_data=[]
    file_path = os.path.join(settings.BASE_DIR,'currencies.json') ## it will look for folder we want and the file we want to join. It basically returns the abs path to the file
            ### we need to access and read the file
    with open(file_path,'r') as json_file:
        data=json.load(json_file) ## with this we can actually read the file . so basically we convert string to python dictionary
            # import pdb
            # pdb.set_trace()
        for key,val in data.items():
            currency_data.append({'name':key,'value':val})
            # import pdb
            # pdb.set_trace()
            # import pdb  ## python debugger
            # pdb.set_trace() ## Program pauses and we can check what's in our variables 
    checkExists=UserPreference.objects.filter(user=request.user).exists()
    user_preferences=None

    ## if preferences already exists
    if checkExists: 
        user_preferences=UserPreference.objects.get(user=request.user)
    if request.method=="GET":
        return render (request,'preferences/index.html',context={
            'currencies':currency_data,
            'user_preferences':user_preferences,
            'API_KEY':os.environ.get('API_KEY'),})
    else: ## for POST Method
        currency=request.POST['currency'] ## reading it from the options
        if checkExists:
        ## updating if already exists
            user_preferences.currency=currency ## saving the userpreferences currency to a new currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user,currency=currency)
        messages.success(request,'Changes Saved')
        return render (request,'preferences/index.html',context={
            'currencies':currency_data,
            'user_preferences':user_preferences,
            'API_KEY':os.environ.get('API_KEY'),
            })
@login_required(login_url="/authenticationapp/login")
def accountPage(request):
    checkExists=UserPreference.objects.filter(user=request.user).exists()
    user_preferences=None
    user_profile=None
    currency=None
    ## if preferences already exists
    if checkExists: 
        user_profile=UserPreference.objects.get(user=request.user)
        user_preferences=UserPreference.objects.get(user=request.user)
        currency=UserPreference.objects.get(user=request.user).currency

    context={
        'user_profile':user_profile,
        'user':User.objects.get(id=request.user.id),
        'user_preferences':user_preferences,
        'currency':currency,   
    }
    if request.method=="GET":
        if not checkExists:
            messages.info(request,"Please maintain your preferred currency to view your profile")
            return redirect('preferences')
        return render(request,'account/account.html',context)

    if request.method== "POST":
        upload_image=request.FILES.get('uploadImage')
        print(upload_image)
        if not upload_image:
            messages.error(request,"Profile pic is not attached")
            return render(request,'account/account.html',context)
        user_profile=UserPreference.objects.get(user=request.user)
        user_profile.profile_pic=upload_image
        user_profile.save()
        messages.success(request,"Profile Photo updated successfully ") 
        return redirect ('account')

def account_update(request):
    context={
        'user_profile':UserPreference.objects.get(user=request.user),
        'user':User.objects.get(id=request.user.id),
        'fieldValues':request.POST,
    }
    if request.method == "POST":
        phonenumber=request.POST.get('phone_number')
        dob=request.POST.get('dob')
        print(phonenumber)
        print(dob)
        if not phonenumber:
            messages.error(request,"Phone Number is required")
            return render(request,'account/account.html',context)
        if not dob:
            messages.error(request,"Date of Birth is required")
            return render(request,'account/account.html',context) 
        ## Updating 
        user_profile=UserPreference.objects.get(user=request.user)
        user_profile.dob=dob
        print(user_profile.dob)
        user_profile.phone=phonenumber
        user_profile.save()
        messages.success(request,"Profile updated successfully !") 
        return redirect('account')
    


