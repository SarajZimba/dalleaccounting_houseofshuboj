from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.canteen import StudentAttendanceViewSet, StudentAttendanceListCreate, DatewiseStudentAttendanceList, DatewiseStudentAggregateAttendanceList, TestCronjob, CheckoutCanteenBill, CheckoutClassBills, CheckoutClassBillsByMonth

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'studentattendance-canteen', StudentAttendanceViewSet, basename='studentattendanceapi')

urlpatterns = [
    path('create-multiple-attendance', StudentAttendanceListCreate.as_view(), name = 'create-multiple-attendance'),
    path('datefilter-canteen-attendance', DatewiseStudentAttendanceList.as_view(), name = 'datefilter-canteen-attendance'),
    path('datefilter-aggregate-canteen-attendance', DatewiseStudentAggregateAttendanceList.as_view(), name = 'datefilter-aggregate-canteen-attendance'),
    path('checkout-bill-canteen', CheckoutCanteenBill.as_view(), name = 'checkout-bill-canteen'),
    path('test-cronjob', TestCronjob.as_view(), name = 'test-cronjob'),
    path('checkout-classbills', CheckoutClassBills.as_view(), name = 'checkout-classbills'),
    path('checkout-classbills-by-month/', CheckoutClassBillsByMonth.as_view(), name='checkout-classbills-by-month'),
] + router.urls

from api.views.canteen import VerifyToken

urlpatterns += [
    path('verify-token/', VerifyToken.as_view(), name='verify-token'),
]
from api.views.canteen import StudentsServedData

urlpatterns += [
    path('served-data/', StudentsServedData.as_view(), name='served-data'),
]


from api.views.canteen import MonthlyAttendanceReportAPI  # Import your view

urlpatterns += [
    # Other URL patterns...
    path('monthly-attendance-report/', MonthlyAttendanceReportAPI.as_view(), name='monthly-attendance-report'),
]

from api.views.canteen import ChangeNotChargedtoCharged, ChangeChargedtoNoCharged  # Import your view

urlpatterns += [
    # Other URL patterns...
    path('credit_to_charged/', ChangeNotChargedtoCharged.as_view(), name='credit_to_charged'),
]

urlpatterns += [
    # Other URL patterns...
    path('charged_to_credit/', ChangeChargedtoNoCharged.as_view(), name='charged_to_credit'),
]