from canteen.models import WorkingDays
from rest_framework.serializers import ModelSerializer

class WorkingDaysSerializer(ModelSerializer):

    class Meta:
        model = WorkingDays
        exclude = [
            'created_at', 'updated_at', 'status', 'is_deleted', 'sorting_order', 'is_featured'
        ]