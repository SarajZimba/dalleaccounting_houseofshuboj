from rest_framework import serializers
from employee.models import Employee

from employee.models import Pay_Package, MasterPayPackage

class PayPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay_Package
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
        
class EmployeePayPackageSerializer(serializers.ModelSerializer):
    pay_packages = PayPackageSerializer(many=True, read_only=True, source='pay_package_set')
    class Meta:
        model = Employee
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

from employee.models import DailyAttendance

class DailyAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAttendance
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
        
class MasterPayPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPayPackage
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

from employee.models import tblEmployeeCIT

class tblEmployeeCITSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = tblEmployeeCIT
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def get_employee_name(self, obj):
        return obj.empID.name