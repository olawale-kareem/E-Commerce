from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from income.serializers import IncomeSerializer
from authentication.models import User
from income.models import Income
from income.permissions import IsOwner
# from expenses.pagination import SmallResultsSetPagination


class IncomeListAPIView(ListCreateAPIView):

    serializer_class = IncomeSerializer
    query_set = Income.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)
    # pagination_class = SmallResultsSetPagination

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.query_set.filter(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = IncomeSerializer
    query_set = Income.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.query_set.filter(owner=self.request.user)
    