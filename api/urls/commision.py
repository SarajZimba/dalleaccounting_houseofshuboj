from django.urls import path
from api.views.commision import CreatetblEmpoyeeCommisionAPIView

urlpatterns = [
    path('create-employee-commision/', CreatetblEmpoyeeCommisionAPIView.as_view(), name='create-employee-commision'),
]