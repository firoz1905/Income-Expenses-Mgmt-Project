from django.shortcuts import render,redirect
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Source, UserIncome
from expenses.models import Expense,Category
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
import json
import datetime
import csv
import xlwt
from django.http import JsonResponse,HttpResponse
# Create your views here.

@login_required(login_url="/authenticationapp/login")
def search_income(request):
    if request.method == 'POST':
        ## search_str ,User will be sending a Json. So whatever (request.body) we are sending over the network we are converting it into python dictionary
        search_str=json.loads(request.body).get('searchText','')
        ## search_str will be a dictiornary in which searhText is a key
        print(search_str)
        income=UserIncome.objects.filter(
            amount__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str,owner=request.user) | UserIncome.objects.filter(
            description__icontains = search_str,owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str,owner=request.user)
        data=income.values() 
        return JsonResponse(list(data),safe=False)

@login_required(login_url="/authenticationapp/login")
def index(request):
    categories=Source.objects.all()
    income=UserIncome.objects.filter(owner=request.user)
    ## using paginator we can display how many items for a page
    paginator=Paginator(income,5) ## show only 3 expenses per page
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
        'income':income,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request,'income/index.html',context)

@login_required(login_url="/authenticationapp/login")
def add_income(request):
    sources=Source.objects.all()  
    context={
            'formValues':request.POST,
            'sources':Source.objects.all()
        }
    if request.method=="GET":    
        return render(request,'income/add_income.html',context)
    if request.method=="POST":
        amount=request.POST['amount']
        date=request.POST['income_date']
        description=request.POST['description']
        source=request.POST['source']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'income/add_income.html',context)
        if not description:
            messages.error(request,"Description is required")
            return render(request,'income/add_income.html',context)
        newincome=UserIncome.objects.create(owner=request.user,amount=amount,date=date,description=description,source=source)
        messages.success(request,"Record saved successfully !")
        return redirect('income')

@login_required(login_url="/authenticationapp/login")
def income_edit(request,id):
    income=UserIncome.objects.get(id=id)
    sources=Source.objects.all()
    context={
        'income':income,
        'formValues':income, ## previous expense information
        'sources':sources,
    }
    if request.method=="GET":
        return render(request,'income/edit_income.html',context)
    if request.method == 'POST':
        amount=request.POST['amount']
        date=request.POST['income_date']
        description=request.POST['description']
        source=request.POST['source']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'income/edit_income.html',context)
        if not description:
            messages.error(request,"Description is required")
            return render(request,'income/edit_income.html',context)
        ## Updating
        income.owner=request.user
        income.amount=amount
        income.description=description
        income.source=source
        income.save()
        messages.success(request,"Income updated successfully !")
        return redirect('income')

@login_required(login_url="/authenticationapp/login")
def delete_income(request,id):
    income=UserIncome.objects.get(id=id)
    income.delete()
    messages.success(request,"Income Removed")
    return redirect ('income')

def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    ## file name
    response['Content-Disposition']='attachment; filename=Incomes' + str(datetime.datetime.now())+ '.csv'
    writer = csv.writer(response)
    ## Header Information
    writer.writerow(['Amount','Description','source','Date'])
    incomes=UserIncome.objects.filter(owner=request.user)
    for income in incomes:
        writer.writerow([income.amount,income.description,income.source,income.date])
    
    return response

def export_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    ## file name
    response['Content-Disposition']='attachment; filename=Incomes' + str(datetime.datetime.now())+ '.xls'
    workBook=xlwt.Workbook(encoding="utf-8")
    workSheet=workBook.add_sheet('Incomes')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Description','source','Date']
    ## Header Information
    for col_num in range(len(columns)):
        workSheet.write(row_num,col_num,columns[col_num],font_style)
    rows=UserIncome.objects.filter(owner=request.user).values_list('amount','description','source','date')
    print(rows)
    for row in rows :
        row_num+=1

        for col_num in range(len(row)):
            workSheet.write(row_num,col_num,str(row[col_num]),font_style)
    workBook.save(response)
    return response

@login_required(login_url="/authenticationapp/login")
def stats_view(request):
    return render(request,'income/stats.html')

@login_required(login_url="/authenticationapp/login")
def income_vs_expenses_stats(request):
    if request.method=="GET":
        total_income=UserIncome.objects.aggregate(total_incomes=Sum('amount'))
        total_expense=Expense.objects.aggregate(total_expenses=Sum('amount'))
        finalrep={}
        finalrep={'total_income':total_income, 'total_expense':total_expense}
        print(finalrep)

        return JsonResponse({'income_expense_data':finalrep},safe=False)

@login_required(login_url="/authenticationapp/login")
def income_source_summary(request):
    if request.method=="GET":
        todays_date=datetime.date.today()
        ## what date it was six months ago
        six_months_ago=todays_date-datetime.timedelta(days=30*6)
        print(six_months_ago)
        ## now query the user incomes during this period .gte (django filters)---> greater than equal to
        incomes=UserIncome.objects.filter(
            owner=request.user,
            date__gte=six_months_ago,
            date__lte=todays_date)
        finalrep={}
        def get_source(income):
            return income.source

        ### It will remove the duplicates as two incomes will be from same source
        source_list = set (map(get_source,incomes))
        print(source_list)

        def get_income_source_amount(source):
            amount=0
            filtered_by_source=incomes.filter(source=source)
            for item in filtered_by_source:
                amount+=item.amount
            return amount
        for x in incomes:
            for y in source_list:
                finalrep[y]= get_income_source_amount(y)
        
        return JsonResponse({'income_source_data':finalrep},safe=False)