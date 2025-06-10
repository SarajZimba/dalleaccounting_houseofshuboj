from django.urls import path
from api.views.purchase import CreatePurchaseAPIView, DeletePurchaseAPIView, InsertPurchaseDetails, ProductPurchaseAPI



urlpatterns = [
    path('purchase-create/', CreatePurchaseAPIView.as_view(), name='purchase-create-api'),
    path('purchase-delete/', DeletePurchaseAPIView.as_view(), name='purchase-delete-api'),

]

urlpatterns += [
    path('purchase-insert/', InsertPurchaseDetails.as_view(), name='purchase-insert'),

]

urlpatterns += [
    path('productpurchase-insert/', ProductPurchaseAPI.as_view(), name='productpurchase-insert'),

]