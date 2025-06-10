# urls.py
from django.urls import path
from api.views.section import CustomerSectionList

urlpatterns = [
    path('sections/', CustomerSectionList.as_view(), name='customer-sections'),
]