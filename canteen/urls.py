
from django.urls import path

from .views import StudentCanteenAttendanceList,StudentCanteenAttendanceDetail,StudentCanteenAttendanceCreate,StudentCanteenAttendanceUpdate,StudentCanteenAttendanceDelete
urlpatterns = [
path('studentcanteenattendance/', StudentCanteenAttendanceList.as_view(), name='studentcanteenattendance_list'),
path('studentcanteenattendance/<int:pk>/', StudentCanteenAttendanceDetail.as_view(), name='studentcanteenattendance_detail'),
path('studentcanteenattendance/create/', StudentCanteenAttendanceCreate.as_view(), name='studentcanteenattendance_create'),
path('studentcanteenattendance/<int:pk>/update/', StudentCanteenAttendanceUpdate.as_view(), name='studentcanteenattendance_update'),
path('studentcanteenattendance/delete', StudentCanteenAttendanceDelete.as_view(), name='studentcanteenattendance_delete')
]

from .views import bill_details_view, print_multiple_bills,single_bill_detail_view
urlpatterns += [
    path('canteen-invoice', bill_details_view, name='canteen-invoice'),
    path('print-multiple-bill/<str:pk>', print_multiple_bills, name='print-multiple-bills'),
    path('single-bill-detail/<int:pk>', single_bill_detail_view, name='single-bill-detail'),
]

from .views import generate_login_token_and_redirect
urlpatterns += [
    path('generate_login_token_and_redirect', generate_login_token_and_redirect, name='generate_login_token_and_redirect'),
]

