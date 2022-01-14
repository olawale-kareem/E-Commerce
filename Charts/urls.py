from .views import ExpensesSummaryStats, IncomeSummaryStats
from django.urls import path


urlpatterns = [
    path('expense_category_data', ExpensesSummaryStats.as_view(),
         name='expense-category-summary'),

    path('income_sources_data', IncomeSummaryStats.as_view(),
         name='IncomeSummaryStats')
]
