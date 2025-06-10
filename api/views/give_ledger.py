from rest_framework import viewsets
from accounting.models import AccountLedger
from api.serializers.give_ledger import AccountLedgerSerializer

from rest_framework.pagination import PageNumberPagination

class NoPagination(PageNumberPagination):
    page_size = None

class AccountLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccountLedger.objects.all()
    serializer_class = AccountLedgerSerializer
    pagination_class = NoPagination
