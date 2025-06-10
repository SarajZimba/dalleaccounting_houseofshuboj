from django.urls import path
from api.views.deduction import DeductionCreateView

urlpatterns = [
    path('deductions/', DeductionCreateView.as_view(), name='deduction-create'),
]
