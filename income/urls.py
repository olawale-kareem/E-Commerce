from django.urls import path
from income import views

urlpatterns = [
    path('',views.IncomeListAPIView.as_view(), name='income'),
    path('<int:id>',views.IncomeDetailAPIView.as_view(), name='income-detail'),
]
