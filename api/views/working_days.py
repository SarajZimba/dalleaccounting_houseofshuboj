from rest_framework.views import APIView

from rest_framework.response import Response

from canteen.models import WorkingDays
from rest_framework.permissions import IsAuthenticated

from api.serializers.working_days import WorkingDaysSerializer

# class WorkingDaysAPI(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         serializer = WorkingDaysSerializer(data=data, many=True)

#         try:
#             if serializer.is_valid():
#                 serializer.save()   
#                 return Response({"data":"date has been posted"}, 200)
#         except Exception as e :
#             return Response({"error": str(e) }, 400)

from datetime import datetime, timedelta
from django.db import transaction

class WorkingDaysAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            data = [data]  # Ensure data is always a list

        # First validate all dates and collect unique months
        months_to_process = set()
        valid_dates = []
        errors = []
        
        for idx, item in enumerate(data):
            try:
                date_str = item.get('working_date')
                if not date_str:
                    errors.append(f"Item {idx}: Missing working_date")
                    continue
                    
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                month_key = (date_obj.year, date_obj.month)
                months_to_process.add(month_key)
                valid_dates.append({'working_date': date_obj})
            except ValueError:
                errors.append(f"Item {idx}: Invalid date format for '{date_str}'. Expected YYYY-MM-DD")
            except Exception as e:
                errors.append(f"Item {idx}: {str(e)}")

        if errors:
            return Response({"errors": errors}, status=400)

        # Delete existing working days for these months
        for year, month in months_to_process:
            month_start = datetime(year, month, 1).date()
            if month == 12:
                month_end = datetime(year+1, 1, 1).date() - timedelta(days=1)
            else:
                month_end = datetime(year, month+1, 1).date() - timedelta(days=1)
            
            WorkingDays.objects.filter(
                working_date__gte=month_start,
                working_date__lte=month_end
            ).delete()

        # Create new working days
        serializer = WorkingDaysSerializer(data=valid_dates, many=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Working days updated successfully",
                    "months_updated": [f"{year}-{month:02d}" for year, month in months_to_process],
                    "count": len(valid_dates)
                }, status=200)
            else:
                return Response({"errors": serializer.errors}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


from datetime import datetime

# class HolidayAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         data = request.data  # Expecting a list of date strings
#         failed_dates = []

#         for datum in data:
#             try:
#                 # Validate date format (optional but good practice)
#                 date_obj = datetime.strptime(datum, "%Y-%m-%d").date()
#                 working_day = WorkingDays.objects.filter(working_date=date_obj)
#                 if working_day.exists():
#                     working_day.delete()
#             except ValueError:
#                 failed_dates.append(datum)

#         if failed_dates:
#             return Response({"error": f"Invalid date format for: {failed_dates}"}, status=400)

#         return Response({"message": "Holidays have been added"}, status=200)

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from bill.models import Bill  # adjust import to your project’s layout

class HolidayAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        raw_dates = request.data  # expecting something like ["2025-05-08", "2025-05-09", ...]
        date_objs = []
        failed_dates = []

        # 1) parse & validate all dates
        for date_str in raw_dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                date_objs.append(date_obj)
            except ValueError:
                failed_dates.append(date_str)

        if failed_dates:
            return Response(
                {"error": f"Invalid date format for: {failed_dates}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not date_objs:
            return Response(
                {"error": "No valid dates provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) extract month & year from the first date
        first = date_objs[0]
        month, year = first.month, first.year

        # 3) check for existing Bill for that month/year
        if Bill.objects.filter(month=month, year=year).exists():
            return Response(
                {"error": f"A bill already exists for {year}-{month:02d}."},
                status=status.HTTP_409_CONFLICT
            )

        # 4) delete any WorkingDays entries for each holiday date
        for date_obj in date_objs:
            WorkingDays.objects.filter(working_date=date_obj).delete()

        # 5) return success
        return Response(
            {"message": f"Holidays for {year}-{month:02d} have been applied."},
            status=status.HTTP_200_OK
        )
        