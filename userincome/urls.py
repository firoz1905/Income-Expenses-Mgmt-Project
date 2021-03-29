from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt,csrf_protect

urlpatterns = [
    path('',views.index,name="income"),
    path('add-income',views.add_income, name="add-income"),
    path('edit-income/<int:id>',views.income_edit,name="income-edit"),
    path('delete-income/<int:id>',views.delete_income,name="income-delete"),
    path('search-income',csrf_exempt(views.search_income), name="search-income"),
    path('income-source-summary',views.income_source_summary,name="income-source-summary"),
    path('income-vs-expenses-stats',views.income_vs_expenses_stats,name="income_vs_expenses_stats"),
    path('stats',views.stats_view,name='stats_income'),
    path('export-csv',views.export_csv,name='export-csv'),
    path('export-excel',views.export_excel,name='export-excel'),
]