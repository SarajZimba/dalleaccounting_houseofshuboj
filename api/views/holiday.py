from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, timedelta
import calendar
from canteen.models import WorkingDays, MonthlyAdjustments

# class HolidayDatesView(APIView):
#     def get(self, request):
#         today = date.today()

#         # Get year and month from query parameters, fallback to current year/month
#         year = int(request.GET.get('year', today.year))
#         month = int(request.GET.get('month', today.month))

#         # Get number of days in the current month
#         _, num_days = calendar.monthrange(year, month)

#         # All dates in current month
#         all_dates = {date(year, month, day) for day in range(1, num_days + 1)}

#         # Dates that are in the WorkingDays table
#         working_dates = set(
#             WorkingDays.objects.filter(
#                 working_date__year=year,
#                 working_date__month=month,
#                 working_date__isnull=False
#             ).values_list('working_date', flat=True)
#         )

#         # Dates that are NOT in working_dates => Holidays
#         holiday_dates = sorted(all_dates - working_dates)

#         # Get MonthlyAdjustments holidays for the month
#         monthly_adjustments = MonthlyAdjustments.objects.filter(
#             year=year,
#             month=month
#         ).values('holiday_date', 'considered_next_month')

#         # Serialize adjustments
#         # adjustments_data = [
#         #     {
#         #         adj['holiday_date'].isoformat(),
#         #     }
#         #     for adj in monthly_adjustments
#         # ]
#         adjustments_data = []

#         for adj in monthly_adjustments:
#             # adj['holiday_date'].isoformat() for adj in holiday_dates
#             adjustments_data.append(adj["holiday_date"])
#         return Response({
#             'holidays': [d.isoformat() for d in holiday_dates],
#             'working_days' : [d.isoformat() for d in working_dates],
#             'monthly_adjustments': adjustments_data
#         })

class HolidayDatesView(APIView):
    def get(self, request):
        today = date.today()

        # Get year and month from query parameters, fallback to current year/month
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        # Get number of days in the current month
        _, num_days = calendar.monthrange(year, month)

        # All dates in current month
        all_dates = {date(year, month, day) for day in range(1, num_days + 1)}

        # Dates that are in the WorkingDays table
        working_dates = set(
            WorkingDays.objects.filter(
                working_date__year=year,
                working_date__month=month,
                working_date__isnull=False
            ).values_list('working_date', flat=True)
        )

        if working_dates:
            # Dates that are NOT in working_dates => Holidays
            holiday_dates = sorted(all_dates - working_dates)

        else:
            holiday_dates = []
            working_dates = all_dates

        # Get MonthlyAdjustments holidays for the month
        monthly_adjustments = MonthlyAdjustments.objects.filter(
            year=year,
            month=month
        ).values('holiday_date', 'considered_next_month')

        # Serialize adjustments
        # adjustments_data = [
        #     {
        #         adj['holiday_date'].isoformat(),
        #     }
        #     for adj in monthly_adjustments
        # ]
        adjustments_data = []

        for adj in monthly_adjustments:
            # adj['holiday_date'].isoformat() for adj in holiday_dates
            adjustments_data.append(adj["holiday_date"])
        return Response({
            'holidays': [d.isoformat() for d in holiday_dates],
            'working_days' : [d.isoformat() for d in working_dates],
            'monthly_adjustments': adjustments_data
        })
    def put(self, request):
        
        working_day = request.data.get("working_day", None)

        if working_day is None:
            return Response({"data": "Working day not provided"}, 200)


        working_days = WorkingDays.objects.filter(
                working_date=working_day,
                working_date__isnull=False
            )

        if working_days:
            working_days.delete()

            return Response({"data": "Working day deleted successfully"}, 200)
        else:
            return Response({"error": "Working day not found"}, 400)
