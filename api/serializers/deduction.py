from rest_framework import serializers
from employee.models import tblDeduction

class tblDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblDeduction
        fields = ['id', 'name', 'used']
