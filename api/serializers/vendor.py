from purchase.models import Vendor
from rest_framework.serializers import ModelSerializer

class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        exclude = [
            'created_at', 'updated_at', 'status', 'is_deleted', 'sorting_order', 'is_featured'
        ]

        