from rest_framework.serializers import ModelSerializer
from bill.models import BillItem, Bill
from rest_framework import serializers
class StudentBillItemSerializer(ModelSerializer):
    product_title = serializers.SerializerMethodField()
    class Meta:
        model = BillItem
        fields = [
            "product_quantity",
            "product",
            "rate",
            "amount",
            "product_title"
        ]
    
    def get_product_title(self, obj):
        return obj.product.title if obj.product else None

from bill.models import BillPayment
class StudentBillPaymentSerializer(ModelSerializer):
    class Meta:
        model = BillPayment
        fields = ['payment_mode', 'rrn', 'amount']
        
from bill.models import MobilePaymentSummary
class StudentMobilePaymentSummarySerializer(ModelSerializer):
    class Meta:
        model = MobilePaymentSummary
        fields = [
            "type",
            "value"
        ]

class StudentBillSerializer(ModelSerializer):
    bill_items = StudentBillItemSerializer(many=True)

    agent = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    split_payment = StudentBillPaymentSerializer(many=True, write_only=True)

    mobile_payments = StudentMobilePaymentSummarySerializer(many=True, write_only=True, required=False)


    class Meta:
        model = Bill
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "organization",
        ]