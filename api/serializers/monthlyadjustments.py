# serializers.py
from rest_framework import serializers
from canteen.models import MonthlyAdjustments

class MonthlyAdjustmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyAdjustments
        fields = ['id','holiday_date', 'considered_next_month', 'month', 'year', 'valid_for_month', 'valid_for_year']
        read_only_fields = ['month', 'year', 'valid_for_month', 'valid_for_year']

    def create(self, validated_data):
        holiday_date = validated_data.get('holiday_date')
        if holiday_date:
            validated_data['month'] = holiday_date.month
            validated_data['year'] = holiday_date.year

            # Calculate valid_for_month and valid_for_year
            if holiday_date.month == 12:
                validated_data['valid_for_month'] = 1
                validated_data['valid_for_year'] = holiday_date.year + 1
            else:
                validated_data['valid_for_month'] = holiday_date.month + 1
                validated_data['valid_for_year'] = holiday_date.year

        return MonthlyAdjustments.objects.create(**validated_data)
