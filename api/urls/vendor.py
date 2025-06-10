from django.urls import path
from api.views.vendor import VendorCreateAPIView

urlpatterns = [

        path("createpurchasevendor", VendorCreateAPIView.as_view(), name="create-vendor")
] 