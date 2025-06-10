from django.urls import path
from api.views.monthlyadjustments import MonthlyAdjustmentView, RemoveMonthlyAdjustmentView

urlpatterns = [
    path('monthlyadjustments-credit/', MonthlyAdjustmentView.as_view(), name='monthy-adjustments'),
    path('remove-monthlyadjustments-credit/', RemoveMonthlyAdjustmentView.as_view(), name='remove-monthlyadjustments-credit'),
]