from django.urls import path
from api.views.salary_sheet import SalarySheet,SalarySlip, MonthlySalaryReportCreateView, GetMonthlySalaryReportAPIView, GetOneYearMonthWiseSalaryReportAPIView
urlpatterns = [
    path("salarysheet/", SalarySheet.as_view(), name="salary_sheet"),
    path("salaryslip/", SalarySlip.as_view(), name="salary_slip")
]
urlpatterns += [
    path("save_salarysheet/", MonthlySalaryReportCreateView.as_view(), name="save_salary_sheet"),
    path("get_monthlysalarysheet/", GetMonthlySalaryReportAPIView.as_view(), name="get_monthlysalary_sheet"),
    path("get_employee_oneyearmonthwisesalarysheet/", GetOneYearMonthWiseSalaryReportAPIView.as_view(), name="get_employee_oneyearmonthwisesalarysheet"),

]
