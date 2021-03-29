from decimal import Context
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
import json
## imports required for Email Messages to sent
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError ### This enables us to create the formats,to send over  the network
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode ## encode and decode the user id
from django.contrib.sites.shortcuts import get_current_site ### construct the domain like a path to our webserver
from django.urls import reverse 
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

### imports from login
from django.contrib import auth


# Create your views here.
### class based Views
class RegistrationView(View):
    def get(self,request):
        return render(request,'authenticationapp/register.html')
    
    def post(self,request):
        ## 1. GET USERDATA
        ## 2. VALIDATE
        ## 3. Create a user Account
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        context={
            'fieldValues':request.POST ### These are the values entered and we want to retain
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,"Password too short")
                    return render(request,'authenticationapp/register.html',context)
                newUser = User.objects.create_user(username=username,email=email)
                newUser.set_password(password)
                ## Before Saving the new user in the database.we first deactive his account and then save so he cannot login
                newUser.is_active = False 
                newUser.save()
                ## what we need in the contents of the email body - We are going to send a link for activating the user account
                #1.- Getting the Domain we are on , then 
                #2.- concatenate the Relative URL ( user account verification)
                #3.- encode user id (identify the user back and forth when clicks on the link)
                #4.- Get token for verification ( We should use the token in a way that we will be using it only once)
                uidb64 = urlsafe_base64_encode(force_bytes(newUser.pk)) ## force_bytes will help to send it through the network
                domain=get_current_site(request).domain ## This will be like if we ever get  a domain from godadday then it would be like yourappname.com
                print(domain)
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(newUser)})  
                ## View would be one of the parameter for reverse. 
                ## If we need something similar to url template tag in our code. Reverse function would do that
                print(link)
                activate_url='http://'+domain+link
                print(activate_url)
                email_subject = "Activation required for your QuickBook Expenses Management Account"
                email_body="Hi" + newUser.username + "  Please use this link to verify your account\n " + activate_url
                email = EmailMessage(
                            email_subject, ## Email Subject
                            email_body, ## Email Body
                            'noreply@expenses.com', ## sender
                            [email], ## Receipients which we can get from the form field email
                )
                print(email)
                email.send(fail_silently=False) ## A boolean. When it’s False, send_mail() will raise an smtplib.SMTPException if an error occurs
                messages.success(request,"Account successfully created")
                return render(request,'authenticationapp/register.html')
        return render(request,'authenticationapp/register.html')

### Email Verification via the link
class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            ## First decode the uid
            ## force_text - will give a human readible format
            ## get or decode the userid
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id) ## query from  user from the database
            
            ## check if the User activated already - is already used the link to activate or not
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message'+'User already activated')

            ## If user is already active
            if user.is_active:
                return redirect('login')
            ## If not , activating the user
            user.is_active = True
            user.save()
            messages.success(request,'Account activated successfully')
            return redirect('login')
        except Exception as e:
            pass
        return redirect('login')

### Login View

class LoginView(View):
    def get(self,request):
        return render(request,'authenticationapp/login.html')
    def post(self,request):
        ## get the form values
        username=request.POST['username']
        password=request.POST['password']

        context={
            'fieldValues':request.POST ### These are the values entered and we want to retain
        }

        if username and password :
            loginUser=auth.authenticate(username=username,password=password)
            ## first check he exists and then if he is active
            if loginUser :
                if loginUser.is_active:
                    auth.login(request,loginUser)
                    messages.success(request,'Welcome, '+loginUser.username+' you are logged in ' )
                    return redirect('expenses')
                messages.error(request,'Account is not active, please check your email')
                return render(request,'authenticationapp/login.html')
            messages.error(request,'Invalid credentials,try again')
            return render(request,'authenticationapp/login.html',context)
        
        messages.error(request,'Please fill all the fields')
        return render(request,'authenticationapp/login.html')


## logout view 
class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,"You have been successfully logged out")
        return redirect('login')

### Email validation View
class EmailValidationView(View):
    ### since the user types in something in the username so we consider it as post request
    def post(self,request): 
        #### json.load is used to read the json document from file 
        #### json. loads() method can be used to parse a valid JSON string and convert it into a valid Python Dictionary.
        #### json.dumps takes in a json object and returns a string
        data=json.loads(request.body) ## will return all the data sent by the user from the form
        print(data)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": "email is invalid"},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Sorry email already in use.Choose another one"},status=409) ## 409 code ---- > resource conflicts
        return JsonResponse({"email_valid": True})

### Username Valid Check
class UsernameValidationView(View):
    ### since the user types in something in the username so we consider it as post request
    def post(self,request): 
        #### json.load is used to read the json document from file 
        #### json. loads() method can be used to parse a valid JSON string and convert it into a valid Python Dictionary.
        #### json.dumps takes in a json object and returns a string
        data=json.loads(request.body) ## will return all the data sent by the user from the form
        print(data)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric charaters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username already in use.Choose another one'},status=409) ## 409 code ---- > resource conflicts
        return JsonResponse({'username_valid': True})


class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authenticationapp/reset-password.html')

    def post(self,request):
        email=request.POST['email']
        context={
            'formValues':request.POST,
        }
        if not validate_email(email):
            messages.error(request,'Please Supply a Valid Email')
            return render(request,'authenticationapp/reset-password.html')
        current_site = get_current_site(request)
        user=User.objects.filter(email=email)
        if user.exists():
            email_contents={
                'user':user[0],
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0]),

            }
            link=reverse('reset-user-password',kwargs={'uidb64':email_contents['uid'],'token':email_contents['user']})  
            email_subject="Password reset Instructions"
            reset_url= 'http://'+current_site.domain+link
            email=EmailMessage(
                email_subject,
                'Hi there , Please use the link to reset your password \n' + reset_url,
                'noreply@expenses.com',
                [email],
            )
            email.send(fail_silently=False)
        messages.success(request, "We have sent an email to reset your password")
        return render(request,'authenticationapp/reset-password.html')


class CompletePasswordReset(View):
    def get (self,request,uidb64,token):
        context ={
            'uidb64': uidb64,
            'token' : token,
        }
        return render(request,'authenticationapp/set-new-password.html',context)
    def post(self,request,uidb64,token):

        context ={
            'uidb64': uidb64,
            'token' : token,
        }
        password=request.POST['password']
        password2=request.POST['password2']
        if password != password2:
            messages.error(request,"Passwords donot match")
            return render (request,'authenticationapp/set-new-password.html',context)
        if len(password) < 6 :
            messages.error(request,"Password too short")
            return render (request,'authenticationapp/set-new-password.html',context)

        try :
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull')
            return redirect('login')
        except Exception as identifier:
            messages.info(request,'Something went wrong. Try again')
            return render (request,'authenticationapp/set-new-password-html',context)

        
        
        







