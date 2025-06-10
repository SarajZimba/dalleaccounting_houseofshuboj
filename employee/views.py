from django.shortcuts import render
from django.views import View
# Create your views here.
from employee.models import Employee
from pathlib import Path
import os
from datetime import timedelta
import environ
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


backend_url = env('Url')
class EmployeeView(View):
    # template_name = "employee/employee_list.html"
    def get(self, request, *args, **kwargs):
        return render(request, "employee/employee_list.html", {"url": backend_url})


class EmployeeCreateView(View):
    # template_name = "employee/employee_list.html"
    def get(self, request, *args, **kwargs):
        return render(request, "employee/employee_create.html" , {"url": backend_url})

class EmployeePayPackageView(View):
    # template_name = "employee/pay_package.html"
    def get(self, request, *args, **kwargs):
        return render(request, "employee/pay_package.html", {"url": backend_url})
    
class EmployeeApplyForLeaveView(View):
    # template_name = "employee/pay_package.html"
    def get(self, request, *args, **kwargs):
        return render(request, "employee/employee_leave.html", {"url": backend_url})


class DailyAttendanceView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dailyattendance/dailyattendance_list.html", {"url": backend_url})

class LeaveApplicationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dailyattendance/leaveapplication.html", {"url": backend_url})

class SalarySheetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "salarysheet/salarysheet.html", {"url": backend_url})

class IndividualSalarySlipView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "salarysheet/individualsalaryslip.html", {"url": backend_url})
        
class AddCommisionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "salarysheet/addcommision.html", {"url": backend_url})
        
class GetCIT(View):
    def get(self, request, *args, **kwargs):
        return render(request, "deductions/cit_list.html", {"url": backend_url})
    
class CreateCIT(View):
    def get(self, request, *args, **kwargs):
        return render(request, "deductions/cit_create.html", {"url": backend_url})