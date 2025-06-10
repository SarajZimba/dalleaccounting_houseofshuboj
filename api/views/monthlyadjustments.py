from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.monthlyadjustments import MonthlyAdjustmentsSerializer
from canteen.models import MonthlyAdjustments

class MonthlyAdjustmentView(APIView):
    def post(self, request, format=None):
        adjustment_date = request.data["holiday_date"]

        adjustment_exists = MonthlyAdjustments.objects.filter(holiday_date=adjustment_date).exists()

        if adjustment_exists:
            return Response({"error": "Adjustment already made for given date"}, 400)
        serializer = MonthlyAdjustmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Holiday credit added successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveMonthlyAdjustmentView(APIView):
    def post(self, request):
        print(request.data)
        monthly_adjustment_date = request.data.get("monthly_adjustment_date", None)

        if not monthly_adjustment_date:


            return Response({"error" : "Provide valid date"}, status=status.HTTP_400_BAD_REQUEST)
        
        monthlyadjustment = MonthlyAdjustments.objects.filter(holiday_date=monthly_adjustment_date)

        monthlyadjustment.delete()


        return Response({"data": "Monthlyadjustment deleted successfully"}, 200)