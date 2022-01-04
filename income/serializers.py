from rest_framework import serializers
from income.models import Income
from authentication.models import User

class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ['id', 'date','description','amount','source']

