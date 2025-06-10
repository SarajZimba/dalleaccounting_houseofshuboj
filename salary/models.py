from django.db import models

from root.utils import BaseModel
# Monthly Salary Report for All Employees

from employee.models import Employee


class MonthlySalaryReport(BaseModel):
    month = models.CharField(max_length=50,null=True)  # Example: 'Magh'
    nepali_date = models.CharField(max_length=50,null=True)  # Example: '10 Magh 2081'
    nepali_year = models.CharField(max_length=50,null=True)
    fiscal_year = models.CharField(max_length = 50, null=True, blank=True)


    def __str__(self):
        return f"Monthly Salary Report for {self.month} - {self.nepali_date}"
    
class Total(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthlysalary = models.ForeignKey(MonthlySalaryReport, on_delete=models.CASCADE)

# Employee details
class EmployeeSalary(BaseModel):
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_report = models.ForeignKey(MonthlySalaryReport, on_delete=models.CASCADE, null=True, blank=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

# Pay Packages (Dynamic)
class EmployeeSalaryPayPackage(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.package_name

# Leave Deductions (Dynamic)
class LeaveDeduction(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name='leave_deductions', on_delete=models.CASCADE)
    unpaid_leavesdeduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unpaid_leaves = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Leave Deduction for {self.employee.name}"

# Fund Deductions (Dynamic)
class FundDeduction(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name='fund_deductions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

# Tax Deductions (Dynamic)
class TaxDeduction(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name='tax_deductions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


