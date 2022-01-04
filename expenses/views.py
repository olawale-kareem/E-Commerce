from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from expenses.serializers import ExpensesSerializer
from authentication.models import User
from expenses.models import Expense
from expenses.permissions import IsOwner
# from expenses.pagination import SmallResultsSetPagination


class ExpensesListAPIView(ListCreateAPIView):

    serializer_class = ExpensesSerializer
    query_set = Expense.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)
    # pagination_class = SmallResultsSetPagination

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.query_set.filter(owner=self.request.user)


class ExpensesDetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = ExpensesSerializer
    query_set = Expense.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.query_set.filter(owner=self.request.user)
    