from rest_framework import serializers
from employee.models import tblEmployeeCommision

class tblEmployeeCommisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblEmployeeCommision
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]