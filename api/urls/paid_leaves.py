from django.urls import path
from api.views.paid_leaves import tblcompanypaidleavePolicyCreateAPIView,tblleaveapplyCreateAPIView, GetEmploeeNoofPaidLeavesApiView, tblleaveapplyListAPIView, confirmleaveapplyAPIView, tblleaveapplyUpdateAPIView, tblleaveapplyCancelAPIView, GetEmployeePaidLeaves



urlpatterns = [
    path('paid-leave-policy/', tblcompanypaidleavePolicyCreateAPIView.as_view(), name='paid-leave-policy'),
    path('leave-apply/', tblleaveapplyCreateAPIView.as_view(), name='leave-apply'),
    path('get-leave-apply/', tblleaveapplyListAPIView.as_view(), name='get-leave-apply'),
    path('confirm-leave-apply/', confirmleaveapplyAPIView.as_view(), name='confirm-leave-apply'),
    path('get-employee-paidleaves/', GetEmploeeNoofPaidLeavesApiView.as_view(), name='get-employee-paidleaves'),
    path('update-tbleaveapply/', tblleaveapplyUpdateAPIView.as_view(), name='update-tbleaveapply'),
    path('cancel-tbleaveapply/', tblleaveapplyCancelAPIView.as_view(), name='cancel-tbleaveapply'),
    path('get-paid-leaves/', GetEmployeePaidLeaves.as_view(), name='get-paid-leaves'),

]
