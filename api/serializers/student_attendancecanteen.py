# serializers.py
from rest_framework import serializers
from canteen.models import PreInformedLeave

class PreInformedLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreInformedLeave
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]