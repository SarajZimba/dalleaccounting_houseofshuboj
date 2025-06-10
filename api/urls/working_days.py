from django.urls import path

from api.views.working_days import WorkingDaysAPI, HolidayAPI

urlpatterns = [
    path('post-workingdays', WorkingDaysAPI.as_view(), name="post-workingdays" ),
    path('add-holiday', HolidayAPI.as_view(), name="add-holiday" )
] 