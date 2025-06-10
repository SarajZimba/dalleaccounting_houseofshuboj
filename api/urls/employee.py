from django.urls import path
from api.views.employee import EmployeeGetAPIView, EmployeeCreateAPIView, EmployeeDetailAPIView, SearchEmployeeAPIView, DailyAttendanceCreateAPIView, DailyAttendanceDetailAPIView, EmployeesDailyAttendanceGetAPIView, GetCheckinOutStatus, GetAllDailyAttendance, AllEmployeeGetAPIView

urlpatterns = [
    path('get-employees/', EmployeeGetAPIView.as_view(), name='get-employees'),
    path('get-all-employees/', AllEmployeeGetAPIView.as_view(), name='get-all-employees'),
    path('employee-create/', EmployeeCreateAPIView.as_view(), name='employee-create'),
    path('search-employee/', SearchEmployeeAPIView.as_view(), name='search-employee' ),
    path('daily-attendance/', GetCheckinOutStatus.as_view(), name="daily-attendance"),
    path('all-daily-attendance/', GetAllDailyAttendance.as_view(), name="all-daily-attendance"),
    path('employee-detail/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('daily_attendance-create/', DailyAttendanceCreateAPIView.as_view(), name='daily-attendance-create'),
    path('daily_attendance-detail/<int:pk>/', DailyAttendanceDetailAPIView.as_view(), name='daily-attendance-detail'),
    path('employees_daily_attendance/', EmployeesDailyAttendanceGetAPIView.as_view(), name='employees-daily-attendance'),

]

from api.views.employee import PayPackageCreateAPIView, RemovePayPackage

urlpatterns += [
    path('paypackage-create/', PayPackageCreateAPIView.as_view(), name='paypackage-create'),
    path('paypackage-remove/', RemovePayPackage.as_view(), name='paypackage-remove'),    
]

from api.views.employee import MasterPayPackageListAPIView

urlpatterns += [
    path('masterpaypackage-list/', MasterPayPackageListAPIView.as_view(), name='masterpaypackage-list'),
]


from api.views.employee import CheckinTime

urlpatterns += [
    path('get-arrival-time/', CheckinTime.as_view(), name='arrival-time')
]


from api.views.employee import EmployeeCITAPI, UpdateEmployeeCITAPI, DeleteEmployeeCITAPI


urlpatterns += [
    path('employee-cit/', EmployeeCITAPI.as_view(), name='employee-cit'),
    path('employee-cit-update/<int:pk>/', UpdateEmployeeCITAPI.as_view(), name='employee-cit-update'),  # For PUT
    path('employee-cit-delete/<int:pk>/', DeleteEmployeeCITAPI.as_view(), name='employee-cit-delete'),  # For DELETE
]