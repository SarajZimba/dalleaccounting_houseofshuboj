from rest_framework import serializers
from salary.models import EmployeeSalary, EmployeeSalaryPayPackage, LeaveDeduction, FundDeduction, TaxDeduction, MonthlySalaryReport

class EmployeeSalaryPayPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalaryPayPackage
        fields = ['package_name', 'amount', 'package_type', 'taxable']

class LeaveDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveDeduction
        fields = ['unpaid_leavesdeduction', 'unpaid_leaves']

class FundDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundDeduction
        fields = ['name', 'amount']

class TaxDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeduction
        fields = ['name', 'total']

class EmployeeSalarySerializer(serializers.ModelSerializer):
    paypackages = EmployeeSalaryPayPackageSerializer(many=True)
    leave_deductions = LeaveDeductionSerializer()
    fund_deductions = FundDeductionSerializer(many=True)
    tax_deductions = TaxDeductionSerializer(many=True)
    
    class Meta:
        model = EmployeeSalary
        fields = ['empID', 'name', 'total_salary', 'paypackages', 'leave_deductions', 'fund_deductions', 'tax_deductions']
