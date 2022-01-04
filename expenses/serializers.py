from rest_framework import serializers
from expenses.models import Expense
from authentication.models import User

class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ['id','date','description','amount','category']
