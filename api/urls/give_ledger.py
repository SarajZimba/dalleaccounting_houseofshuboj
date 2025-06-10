from django.urls import path
from api.views.give_ledger import AccountLedgerViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register("ledgers", AccountLedgerViewSet)

urlpatterns = [] + router.urls