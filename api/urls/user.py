from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers

from ..views.user import CustomTokenObtainPairView, CustomerAPI

from ..views.user import AgentViewSet


router = routers.DefaultRouter()
router.register('agent-create', AgentViewSet, basename='agent')


router.register("customer", CustomerAPI)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls

from api.views.user import PostCustomerListAPI
urlpatterns += [
    path("customerlist-create/", PostCustomerListAPI.as_view(), name="customerlist-create")
]

from api.views.user import DeleteCustomerAPI
urlpatterns += [
    path("delete-customer/", DeleteCustomerAPI.as_view(), name="delete-customer")
]

from api.views.user import UpdateCustomerStudentClass
urlpatterns += [
    path("update-class/", UpdateCustomerStudentClass.as_view(), name="update-class")
]

from api.views.user import StatusToggleStudent, StudentsAPI
urlpatterns += [
    path("status-toggle-customer/", StatusToggleStudent.as_view(), name="status-toggle-customer/"),
    path("student-lists/", StudentsAPI.as_view(), name="student-lists/"),
]