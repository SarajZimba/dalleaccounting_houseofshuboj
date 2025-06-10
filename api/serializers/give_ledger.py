from rest_framework import serializers
from accounting.models import AccountLedger

class AccountLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLedger
        fields = ('id', 'ledger_name')
