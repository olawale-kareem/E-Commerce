from .views import ExpensesSummaryStats
from django.urls import path


urlpatterns = [
    path('expense_category_data', ExpensesSummaryStats.as_view(),
         name='expense-category-summary')
]
