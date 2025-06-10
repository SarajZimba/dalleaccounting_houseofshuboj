from django.urls import path
from .views import EmployeeView, EmployeeCreateView,EmployeePayPackageView,EmployeeApplyForLeaveView

urlpatterns = [
    path("employee-list/", EmployeeView.as_view(),name="employee-list"),
    path('employee-create/',EmployeeCreateView.as_view(), name='employee-create-page'),
    path('employee-paycheck-view/',EmployeePayPackageView.as_view(), name='employee-paycheck-page'),
    path('employee-leave-view/',EmployeeApplyForLeaveView.as_view(), name='employee-leave-page'),

]
    
from .views import DailyAttendanceView,LeaveApplicationView

urlpatterns += [
    path("dailyattendance-list/", DailyAttendanceView.as_view(),name="dailyattendance-list"),
    path("leaveapplication/", LeaveApplicationView.as_view(),name="leaveapplication"),


]
from .views import SalarySheetView,IndividualSalarySlipView, AddCommisionView

urlpatterns += [
    path("salarysheet/", SalarySheetView.as_view(),name="salarysheet"),
    path("individualsalaryslip/", IndividualSalarySlipView.as_view(),name="individualsalaryslip"),
    path("addcommision/", AddCommisionView.as_view(),name="addcommision"),


]

from .views import GetCIT, CreateCIT

urlpatterns += [
    path("get-cit-list/", GetCIT.as_view(),name="get-cit-list"),
    path("create-cit-list/", CreateCIT.as_view(),name="create-cit-list"),

]