from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt,csrf_protect

urlpatterns = [
    path('',views.index,name="expenses"),
    path('add-expense',views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>',views.expense_edit,name="expense-edit"),
    path('delete-expense/<int:id>',views.delete_expense,name="expense-delete"),
    path('search-expenses',csrf_exempt(views.search_expenses), name="search-expenses"),
    path('expense-category-summary',views.expense_category_summary,name="expense_category_summary"),
    path('stats',views.stats_view,name='stats'),
    path('export-csv',views.export_csv,name='export-csv'),
    path('export-excel',views.export_excel,name='export-excel'),
    path('expense-category-distribution',views.expense_category_distribution,name="expense_category_distribution"),
    path('category-cummulative-comparison',views.category_cummulative_comparison,name="category_cummulative_comparison"),
]
