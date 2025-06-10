from product.models import Product
from rest_framework import serializers
from canteen.models import StudentAttendance

class StudentAttendanceSerializer(serializers.ModelSerializer):
    roll_no = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    student_class = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    
    # product_rate = serializers.SerializerMethodField()
    meal_preference = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    


    class Meta:
        model = StudentAttendance
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def get_roll_no(self, obj):
        return obj.student.roll_no if obj.student.roll_no else None
    def get_student_name(self, obj):
        return obj.student.name if obj.student.name else None
    def get_student_class(self, obj):
        return obj.student.student_class if obj.student.student_class else None
    def get_section(self, obj):
        return obj.student.section if obj.student.section else None
    def get_meal_preference(self, obj):
        return obj.student.meal_preference if obj.student.meal_preference else None
    def get_product_name(self, obj):
        return obj.product.title if obj.product.title else None
    # def get_product_rate(self, obj):
    #     item = Product.objects.filter(is_canteen_item=True).first()
    #     return item.price if item else 0.0 
    
from canteen.models import tblmissedattendance
class MissedAttendanceSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    product_rate = serializers.SerializerMethodField()

    class Meta:
        model = tblmissedattendance
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
    def get_product_title(self, obj):
        return obj.product.title if obj.product else None
    
    def get_product_rate(self, obj):
        return obj.product.price if obj.product else None
# api/serializers/canteen.py
from rest_framework import serializers
from canteen.models import MonthlyAdjustments

class MonthlyAdjustmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyAdjustments
        fields = '__all__'
        
from canteen.models import tblmissedattendance_butcharged
class MissedButChargedSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    product_rate = serializers.SerializerMethodField()

    class Meta:
        model = tblmissedattendance_butcharged
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
    def get_product_title(self, obj):
        return obj.product.title if obj.product else None
    
    def get_product_rate(self, obj):
        return obj.product.price if obj.product else None