from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category,Expense
from userpreferences.models import UserPreference
from django.core.paginator import Paginator 
import json
from django.http import JsonResponse,HttpResponse ## to format json content back to user
import datetime
import csv 
import xlwt
import pandas as pd
from dateutil.rrule import *
from datetime import date
from time import strftime, strptime
## xlwt for excel . pip install xlwt

# Create your views here.
@login_required(login_url="/authenticationapp/login")
def search_expenses(request):
    if request.method == 'POST':
        ## search_str ,User will be sending a Json. So whatever (request.body) we are sending over the network we are converting it into python dictionary
        search_str=json.loads(request.body).get('searchText','')
        ## search_str will be a dictiornary in which searhText is a key
        print(search_str)
        expenses=Expense.objects.filter(
            amount__istartswith=search_str,owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str,owner=request.user) | Expense.objects.filter(
            description__icontains = search_str,owner=request.user) | Expense.objects.filter(
            category__icontains=search_str,owner=request.user)
        data=expenses.values() 
        return JsonResponse(list(data),safe=False)


@login_required(login_url="/authenticationapp/login")
def index(request):
    categories=Category.objects.all()
    expenses=Expense.objects.filter(owner=request.user)
    ## using paginator we can display how many items for a page
    paginator=Paginator(expenses,5) ## show only 5 expenses per page
    print(paginator)
    ## query the paginator object for a specific page
    page_number=request.GET.get('page')
    print(page_number)
    ## construct the page object. This would section the expenses into different pages
    page_obj=Paginator.get_page(paginator,page_number)
    print(page_obj)
    ## get the curency information of user preferences models
    checkExists=UserPreference.objects.filter(user=request.user).exists()
    currency=None
    if checkExists:
        currency=UserPreference.objects.get(user=request.user).currency
    print(currency)
    context={
        'categories':categories,
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request,'expenses/index.html',context)

@login_required(login_url="/authenticationapp/login")
def add_expense(request):
    categories=Category.objects.all()  
    context={
            'formValues':request.POST,
            'categories':Category.objects.all()
        }
    if request.method=="GET":    
        return render(request,'expenses/add_expense.html',context)
    if request.method=="POST":
        amount=request.POST['amount']
        date=request.POST['expense_date']
        description=request.POST['description']
        category=request.POST['category']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'expenses/add_expense.html',context)
        if not description:
            messages.error(request,"Description is required")
            return render(request,'expenses/add_expense.html',context)
        newExpense=Expense.objects.create(owner=request.user,amount=amount,date=date,description=description,category=category)
        messages.success(request,"Expense saved successfully !")
        return redirect('expenses')

@login_required(login_url="/authenticationapp/login")
def expense_edit(request,id):
    expense=Expense.objects.get(id=id)
    categories=Category.objects.all()
    context={
        'expense':expense,
        'formValues':expense, ## previous expense information
        'categories':categories,
    }
    if request.method=="GET":
        return render(request,'expenses/edit-expense.html',context)
    if request.method == 'POST':
        amount=request.POST['amount']
        date=request.POST['expense_date']
        description=request.POST['description']
        category=request.POST['category']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'expenses/edit-expense.html',context)
        if not description:
            messages.error(request,"Description is required")
            return render(request,'expenses/edit-expense.html',context)
        ## Updating
        expense.owner=request.user
        expense.amount=amount
        expense.description=description
        expense.category=expense.category
        expense.save()
        messages.success(request,"Expense updated successfully !")
        return redirect('expenses')

@login_required(login_url="/authenticationapp/login")
def delete_expense(request,id):
    expense=Expense.objects.get(id=id)
    expense.delete()
    messages.success(request,"Expense Removed")
    return redirect ('expenses')

def expense_category_summary(request):
    if request.method=="GET":
        todays_date=datetime.date.today()
        ## what date it was six months ago
        six_months_ago=todays_date-datetime.timedelta(days=30*6)
        print(six_months_ago)
        ## now query the user expenses during this period .gte (django filters)---> greater than equal to
        expenses=Expense.objects.filter(
            owner=request.user,
            date__gte=six_months_ago,
            date__lte=todays_date)
        for exp in expenses:
            print(exp.category)
            
        finalrep={}
        def get_category(expense):
            return expense.category
        print(expenses)
        ### It will remove the duplicates as two expenses will have same category
        category_list = set(map(get_category,expenses))
        print(category_list)

        def get_expense_category_amount(category):
            amount=0
            filtered_by_category=expenses.filter(category=category)
            for item in filtered_by_category:
                amount+=item.amount
            return amount
        
        for x in expenses:
            for y in category_list:
                finalrep[y]= get_expense_category_amount(y)
        
        return JsonResponse({'expense_category_data':finalrep},safe=False)

@login_required(login_url="/authenticationapp/login")
def expense_category_distribution(request):
    if request.method=="GET":
        todays_date=datetime.date.today()
        ## what date it was three months ago
        three_months_ago=todays_date-datetime.timedelta(days=30*3)
        print(three_months_ago)
        expenses=Expense.objects.filter(
            owner=request.user,
            date__gte=three_months_ago,
            date__lte=todays_date)
        finalrep={}

        def get_category(expense):
            return expense.category
        ## to get the complete category list of all the expenses we have in our range
        category_list=set(map(get_category,expenses))

        ## now sum the amounts of each category from the list

        def get_expense_category_amount(category):
            amount=0;
            expenses_filtered_by_category=expenses.filter(category=category)
            for item in expenses_filtered_by_category:
                amount+=item.amount
            return amount
        for x in expenses:
            for y in category_list:
                finalrep[y]=get_expense_category_amount(y)
        return JsonResponse({'expense_category_data':finalrep},safe=False)

@login_required(login_url="/authenticationapp/login")
def category_cummulative_comparison(request):
    if request.method=="GET":
        todays_date=datetime.date.today()
        print(todays_date.year)
        ## what date it was three months ago
        three_months_ago=todays_date-datetime.timedelta(days=30*3)
        expenses=Expense.objects.filter(
            owner=request.user,
            date__gte=three_months_ago,
            date__lte=todays_date,)
        print(expenses)
        finalrep={}
        months_list=[]
        for month in months_between(three_months_ago,todays_date):
            months_list.append(month.strftime("%Y,%b,%m"))
        print(months_list)

        def get_category(expense):
            return expense.category
        ## to get the complete category list of all the expenses we have in our range
        category_list=set(map(get_category,expenses))
        print(category_list)

        def get_expense_cummulative_amount(month):
            amount=0;
            expenses_filtered_by_months=expenses.filter(date__month=month)
            for item in expenses_filtered_by_months:
                amount+=item.amount
            return amount        
        for x in expenses:
            for y in months_list:
                year, month_name,month = y.split(',',2)
                finalrep[y]=get_expense_cummulative_amount(month)
        print(finalrep)
        
        return JsonResponse({'expense_cummulative_data':finalrep},safe=False)

@login_required(login_url="/authenticationapp/login")
def stats_view(request):
    return render(request,'expenses/stats.html')


def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    ## file name
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now())+ '.csv'
    writer = csv.writer(response)
    ## Header Information
    writer.writerow(['Amount','Description','category','Date'])
    expenses=Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])
    
    return response

def export_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    ## file name
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now())+ '.xls'
    workBook=xlwt.Workbook(encoding="utf-8")
    workSheet=workBook.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Description','category','Date']
    ## Header Information
    for col_num in range(len(columns)):
        workSheet.write(row_num,col_num,columns[col_num],font_style)
    rows=Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')
    for row in rows :
        row_num+=1

        for col_num in range(len(row)):
            workSheet.write(row_num,col_num,str(row[col_num]),font_style)
    workBook.save(response)
    return response

### Function to calcualte the list of months for a given range

def months_between(start_date, end_date):
    """
    Given two instances of ``datetime.date``, generate a list of dates on
    the 1st of every month between the two dates (inclusive).

    e.g. "5 Jan 2020" to "17 May 2020" would generate:

        1 Jan 2020, 1 Feb 2020, 1 Mar 2020, 1 Apr 2020, 1 May 2020

    """
    if start_date > end_date:
        raise ValueError(f"Start date {start_date} is not before end date {end_date}")

    year = start_date.year
    month = start_date.month

    while (year, month) <= (end_date.year, end_date.month):
        yield datetime.date(year, month, 1)

        # Move to the next month.  If we're at the end of the year, wrap around
        # to the start of the next.
        #
        # Example: Nov 2017
        #       -> Dec 2017 (month += 1)
        #       -> Jan 2018 (end of year, month = 1, year += 1)
        #
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
     


    




        

    
        
        
        
        