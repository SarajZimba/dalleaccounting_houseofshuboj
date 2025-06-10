
from django.urls import path
from api.views.holiday import HolidayDatesView

urlpatterns = [
    path('holidays/', HolidayDatesView.as_view(), name='holiday-dates'),
]
