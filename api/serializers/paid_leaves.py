from rest_framework import serializers

from employee.models import tblcompanypaidleavePolicy, tblleaveapply, tblpaidleaves


class tblcompanypaidleavePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = tblcompanypaidleavePolicy
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

class tblleaveapplySerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = tblleaveapply
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]


    def get_employee_name(self, obj):
        return obj.empID.name if obj.empID else None
        
        
class tblpaidleavesSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = tblpaidleaves
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]


    def get_employee_name(self, obj):
        return obj.empID.name if obj.empID else None