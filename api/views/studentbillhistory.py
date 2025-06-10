from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bill.models import Bill
from api.serializers.studentbillhistory import StudentBillSerializer
from user.models import Customer
from canteen.models import tblmissedattendance, MonthlyAdjustments
from api.serializers.canteen import MissedAttendanceSerializer, MonthlyAdjustmentsSerializer, MissedButChargedSerializer 

# class StudentHistory(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         student_id = request.data.get('student_id')
#         if not Customer.objects.filter(pk=student_id).exists():
#             return Response({"error": "Invalid student id provided"},
#                             status=status.HTTP_400_BAD_REQUEST)

#         student = Customer.objects.get(pk=student_id)

#         # 1) Get and group bills by year-month
#         bills = Bill.objects.filter(
#             customer=student,
#             customer__student_class__isnull=False
#         ).order_by('-year', '-month')
#         bills_data = StudentBillSerializer(bills, many=True).data

#         bills_by_month = defaultdict(list)
#         for b in bills_data:
#             key = f"{b['year']:04d}-{b['month']:02d}"
#             bills_by_month[key].append(b)

#         # 2) Missed Attendance
#         missed_qs = tblmissedattendance.objects.filter(student=student)
#         missed_data = MissedAttendanceSerializer(missed_qs, many=True).data

#         # 3) Missed but charged
#         missed_charged_qs = tblmissedattendance_butcharged.objects.filter(student=student)
#         missed_charged_data = MissedButChargedSerializer(missed_charged_qs, many=True).data

#         # 4) Monthly adjustments
#         adjustments_qs = MonthlyAdjustments.objects.all()  # optionally filter by student
#         adjustments_data = MonthlyAdjustmentsSerializer(adjustments_qs, many=True).data

#         # 5) Combine all into a monthly summary
#         monthly_combined = defaultdict(lambda: {
#             "bills": [],
#             "missed_attendance": 0,
#             "monthly_adjustments": 0,
#             "missed_but_charged": 0
#         })

#         # Add bills
#         for key, bills in bills_by_month.items():
#             monthly_combined[key]["bills"] = bills

#         # Add missed attendance counts
#         for m in missed_data:
#             dt = m['missed_date']  # format: "YYYY-MM-DD"
#             year, month, _ = dt.split('-')
#             key = f"{year}-{month}"
#             monthly_combined[key]["missed_attendance"] += 1

#         # Add missed but charged counts
#         for m in missed_charged_data:
#             dt = m['missed_date']  # format: "YYYY-MM-DD"
#             year, month, _ = dt.split('-')
#             key = f"{year}-{month}"
#             monthly_combined[key]["missed_but_charged"] += 1

#         # Add adjustments count
#         for adj in adjustments_data:
#             year = adj.get('valid_for_year')
#             month = adj.get('valid_for_month')
#             if year is not None and month is not None:
#                 key = f"{year:04d}-{month:02d}"
#                 monthly_combined[key]["monthly_adjustments"] += 1

#         # Optionally sort months descending
#         sorted_monthly_data = dict(sorted(monthly_combined.items(), reverse=True))

#         return Response({
#             "student_monthly_data": sorted_monthly_data
#         }, status=status.HTTP_200_OK)

from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class StudentHistory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        if not Customer.objects.filter(pk=student_id).exists():
            return Response({"error": "Invalid student id provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        student = Customer.objects.get(pk=student_id)

        # 1) Get and group bills by year-month
        bills = Bill.objects.filter(
            customer=student,
            customer__student_class__isnull=False
        ).order_by('-year', '-month')
        bills_data = StudentBillSerializer(bills, many=True).data

        print(bills_data)

        bills_by_month = defaultdict(list)
        for b in bills_data:
            key = f"{b['year']:04d}-{b['month']:02d}"
            bills_by_month[key].append(b)

        # 2) Missed Attendance
        missed_qs = tblmissedattendance.objects.filter(student=student)
        missed_data = MissedAttendanceSerializer(missed_qs, many=True).data

        print(missed_data)

        # 3) Missed but charged
        missed_charged_qs = tblmissedattendance_butcharged.objects.filter(student=student)
        missed_charged_data = MissedButChargedSerializer(missed_charged_qs, many=True).data

        print(missed_charged_data)

        # 4) Monthly adjustments
        adjustments_qs = MonthlyAdjustments.objects.all()  # optionally filter by student
        adjustments_data = MonthlyAdjustmentsSerializer(adjustments_qs, many=True).data

        # 5) Combine all into a monthly summary
        monthly_combined = defaultdict(lambda: {
            "bills": [],
            "missed_attendance": 0,
            "monthly_adjustments": 0,
            "missed_but_charged": 0
        })

        # Add bills
        for key, bills in bills_by_month.items():
            monthly_combined[key]["bills"] = bills

        # Add missed attendance counts (+1 month forward)
        for m in missed_data:
            dt = datetime.strptime(m['missed_date'], "%Y-%m-%d")
            next_month = dt + relativedelta(months=1)
            key = next_month.strftime("%Y-%m")
            monthly_combined[key]["missed_attendance"] += 1

        # Add missed but charged counts (+1 month forward)
        for m in missed_charged_data:
            dt = datetime.strptime(m['missed_date'], "%Y-%m-%d")
            next_month = dt + relativedelta(months=1)
            key = next_month.strftime("%Y-%m")
            monthly_combined[key]["missed_but_charged"] += 1

        # Add adjustments count (in current month)
        for adj in adjustments_data:
            year = adj.get('valid_for_year')
            month = adj.get('valid_for_month')
            if year is not None and month is not None:
                key = f"{year:04d}-{month:02d}"
                monthly_combined[key]["monthly_adjustments"] += 1

        # Sort months descending
        sorted_monthly_data = dict(sorted(monthly_combined.items(), reverse=True))

        return Response({
            "student_monthly_data": sorted_monthly_data
        }, status=status.HTTP_200_OK)

from django.db.models.functions import ExtractMonth, ExtractYear
from canteen.models import StudentAttendance, tblmissedattendance_butcharged
from api.serializers.canteen import StudentAttendanceSerializer
# class StudentHistoryCanteen(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         student_id = request.data.get('student_id')
#         month = int(request.data.get('month'))
#         year = int(request.data.get('year'))

#         if not Customer.objects.filter(pk=student_id).exists():
#             return Response({"error": "Invalid student id provided"},
#                             status=status.HTTP_400_BAD_REQUEST)

#         student = Customer.objects.get(pk=student_id)

#         # ✅ Calculate previous month and year
#         if month == 1:
#             prev_month = 12
#             prev_year = year - 1
#         else:
#             prev_month = month - 1
#             prev_year = year

#         missed_qs = tblmissedattendance.objects.annotate(
#             month=ExtractMonth('missed_date'),
#             year=ExtractYear('missed_date')
#         ).filter(student=student, month=prev_month, year=prev_year)
#         missed_data = MissedAttendanceSerializer(missed_qs, many=True).data

#         adjustments_qs = MonthlyAdjustments.objects.filter(
#             valid_for_month=month,
#             valid_for_year=year
#         )
#         adjustments_data = MonthlyAdjustmentsSerializer(adjustments_qs, many=True).data

#         attendance_qs = StudentAttendance.objects.annotate(
#             month=ExtractMonth('eaten_date'),
#             year=ExtractYear('eaten_date')
#         ).filter(student=student, month=month, year=year)
#         attendance_data = StudentAttendanceSerializer(attendance_qs, many=True).data

#         missed_charged_qs = tblmissedattendance_butcharged.objects.annotate(
#             month=ExtractMonth('missed_date'),
#             year=ExtractYear('missed_date')
#         ).filter(student=student, month=prev_month, year=prev_year)
#         missed_charged_data = MissedButChargedSerializer(missed_charged_qs, many=True).data

#         return Response({
#             "missed_attendance": missed_data,
#             "monthly_adjustments": adjustments_data,
#             "attendance_data": attendance_data,
#             "missed_but_charged": missed_charged_data
#         }, status=status.HTTP_200_OK)
    
class StudentHistoryCanteen(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        month = int(request.data.get('month'))
        year = int(request.data.get('year'))

        if not Customer.objects.filter(pk=student_id).exists():
            return Response({"error": "Invalid student id provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        student = Customer.objects.get(pk=student_id)

        # ✅ Calculate previous month and year
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        missed_qs = tblmissedattendance.objects.annotate(
            month=ExtractMonth('missed_date'),
            year=ExtractYear('missed_date')
        ).filter(student=student, month=prev_month, year=prev_year)
        missed_data = MissedAttendanceSerializer(missed_qs, many=True).data

        adjustments_qs = MonthlyAdjustments.objects.filter(
            valid_for_month=month,
            valid_for_year=year
        )
        adjustments_data = MonthlyAdjustmentsSerializer(adjustments_qs, many=True).data

        attendance_qs = StudentAttendance.objects.annotate(
            month=ExtractMonth('eaten_date'),
            year=ExtractYear('eaten_date')
        ).filter(student=student, month=month, year=year)
        attendance_data = StudentAttendanceSerializer(attendance_qs, many=True).data

        missed_charged_qs = tblmissedattendance_butcharged.objects.annotate(
            month=ExtractMonth('missed_date'),
            year=ExtractYear('missed_date')
        ).filter(student=student, month=prev_month, year=prev_year)
        missed_charged_data = MissedButChargedSerializer(missed_charged_qs, many=True).data

        # Prepare product references
        veg_product = Product.objects.filter(
                is_canteen_item=True, lunch_type="veg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()
        egg_product = Product.objects.filter(
                is_canteen_item=True, lunch_type="egg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()
        nonveg_product = Product.objects.filter(
                is_canteen_item=True, lunch_type="nonveg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()
        for holiday in adjustments_data:
                holiday_date_raw = holiday['holiday_date']
                holiday_date = datetime.strptime(holiday_date_raw, "%Y-%m-%d").date()
                print(holiday_date)
                day_name = holiday_date.strftime("%A")
                preference = student.meal_preference

                product_to_subtract = None

                if day_name == "Wednesday":
                    if preference == "nonveg" and nonveg_product:
                        product_to_subtract = nonveg_product
                        holiday["product_title"] =   product_to_subtract.title
                        holiday["product_rate"] =   product_to_subtract.price
                    else:
                        product_to_subtract = veg_product
                elif day_name == "Friday":
                    if preference in ["egg", "nonveg"] and egg_product:
                        product_to_subtract = egg_product
                        holiday["product_title"] =   product_to_subtract.title
                        holiday["product_rate"] =   product_to_subtract.price

                    else:
                        product_to_subtract = veg_product
                        holiday["product_title"] =   product_to_subtract.title
                        holiday["product_rate"] =   product_to_subtract.price

                else:
                    product_to_subtract = veg_product 
                    holiday["product_title"] =   product_to_subtract.title   
                    holiday["product_rate"] =   product_to_subtract.price
   
        return Response({
            "missed_attendance": missed_data,
            "monthly_adjustments": adjustments_data,
            "attendance_data": attendance_data,
            "missed_but_charged": missed_charged_data
        }, status=status.HTTP_200_OK)

import pytz
from datetime import datetime, timedelta
from nepali_datetime import date as nepali_date
from canteen.models import WorkingDays
from organization.models import Branch, Organization
from product.models import Product
from collections import defaultdict
from canteen.utils import convert_amount_to_words
from bill.models import BillItem

class StudentBillPreview(APIView):

    def post(self, request, *args, **kwargs):

        student_id = request.data.get('student_id')

        print('student_id', student_id)
        if not Customer.objects.filter(pk=int(student_id)).exists():
            return Response({"error": "Invalid student id provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        student = Customer.objects.get(pk=int(student_id))

        month = request.data.get('month')
        year = request.data.get('year')

        nepal_tz = pytz.timezone("Asia/Kathmandu")

        # Calculate month start and end dates for target month
        month_start = datetime(year, month, 1, tzinfo=nepal_tz)
        if month == 12:
            month_end = datetime(year+1, 1, 1, tzinfo=nepal_tz) - timedelta(days=1)
        else:
            month_end = datetime(year, month+1, 1, tzinfo=nepal_tz) - timedelta(days=1)

        # Calculate previous month start and end dates
        if month == 1:
            prev_month_start = datetime(year-1, 12, 1, tzinfo=nepal_tz)
            prev_month_end = month_start - timedelta(days=1)
        else:
            prev_month_start = datetime(year, month-1, 1, tzinfo=nepal_tz)
            prev_month_end = month_start - timedelta(days=1)

        transaction_date_time = datetime.now(nepal_tz).strftime("%Y-%m-%d %H:%M:%S")
        transaction_date = datetime.now(nepal_tz).strftime("%Y-%m-%d")
        transaction_miti = nepali_date.today()

        # Get working days for the target month
        working_days = WorkingDays.objects.filter(
            working_date__gte=month_start.date(),
            working_date__lte=month_end.date()
        ).values_list('working_date', flat=True).order_by('working_date')

        if not working_days.exists():
            message = f"No working days found for {month_start.strftime('%B %Y')}"
            print(message)
            return Response({"success": False, "message": message},status=400)

        branch = Branch.objects.active().filter(is_central_billing=True).last()
        if not branch:
            message = "No central billing branch found"
            return Response({"success": False, "message": message},status=400)

        students = Customer.objects.filter(id=student_id)
        # Subtract holiday meals not yet considered
        unprocessed_holidays = MonthlyAdjustments.objects.filter(
                considered_next_month=False,
                valid_for_month=month,
                valid_for_year=year,
                holiday_date__lte=month_end.date()  # Include previous and current holidays
        )
        for student in students:
            discount_applied = student.discount_applicable
            product_counter = defaultdict(int)

            # Prepare product references
            veg_product = Product.objects.filter(
                is_canteen_item=True, lunch_type="veg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()
            egg_product = Product.objects.filter(
                is_canteen_item=True, lunch_type="egg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()
            nonveg_product = Product.objects.filter(
                is_canteen_item=True, lunch_type="nonveg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()

            if not veg_product or not egg_product or not nonveg_product:
                message = "Required products missing. Cannot proceed."
                print(message)
                return Response({"success": False, "message": message},status=400)

            # Get missed meals from previous month that haven't been considered yet
            missed_meals = tblmissedattendance.objects.filter(
                student=student,
                considered_next_month=False,
                missed_date__gte=prev_month_start.date(),
                missed_date__lte=prev_month_end.date()
            )

            # Count all working days in the target month
            for day in working_days:
                day_name = day.strftime("%A")
                preference = student.meal_preference

                if day_name == "Wednesday":
                    if preference == "nonveg" and nonveg_product:
                        product_counter[nonveg_product.id] += 1
                    else:
                        product_counter[veg_product.id] += 1
                elif day_name == "Friday":
                    if preference in ["egg", "nonveg"] and egg_product:
                        product_counter[egg_product.id] += 1
                    else:
                        product_counter[veg_product.id] += 1
                else:
                    product_counter[veg_product.id] += 1

            # Subtract the missed meals from previous month
            for missed_meal in missed_meals:
                if missed_meal.product:
                    product_id = missed_meal.product.id
                    if product_id in product_counter:
                        product_counter[product_id] -= 1
                        if product_counter[product_id] < 0:
                            product_counter[product_id] = 0
                    missed_meal.considered_next_month = True
                    missed_meal.save()

            for holiday in unprocessed_holidays:
                holiday_date = holiday.holiday_date
                day_name = holiday_date.strftime("%A")
                preference = student.meal_preference

                product_to_subtract = None

                if day_name == "Wednesday":
                    if preference == "nonveg" and nonveg_product:
                        product_to_subtract = nonveg_product
                    else:
                        product_to_subtract = veg_product
                elif day_name == "Friday":
                    if preference in ["egg", "nonveg"] and egg_product:
                        product_to_subtract = egg_product
                    else:
                        product_to_subtract = veg_product
                else:
                    product_to_subtract = veg_product

                if product_to_subtract and product_to_subtract.id in product_counter:
                    product_counter[product_to_subtract.id] -= 1
                    if product_counter[product_to_subtract.id] < 0:
                        product_counter[product_to_subtract.id] = 0

            # Remove products with zero quantity
            product_counter = {k: v for k, v in product_counter.items() if v > 0}

            bill_items = []
            sub_total = 0

            for product_id, quantity in product_counter.items():
                product = Product.objects.filter(id=product_id).first()
                if not product:
                    continue
                rate = float(product.price)
                amount = rate * quantity
                sub_total += amount

                bill_item = {
                    "product_quantity":quantity,
                    "rate":rate,
                    "product_title":product.title,
                    "unit_title":product.unit,
                    "amount":amount,
                    "product":product.id
                }
                bill_items.append(bill_item)



            if discount_applied is not None:
                if discount_applied.discount_type == "PCT":
                    discount_amount = (discount_applied.discount_amount/100) * sub_total
                if discount_applied.discount_type == "FLAT":
                    discount_amount = discount_applied.discount_amount
            else:
                discount_amount = 0.0

            taxable_amount = sub_total - discount_amount
            tax_amount = taxable_amount * 0.13

            grand_total = sub_total + tax_amount - discount_amount
            amount_in_words = convert_amount_to_words(grand_total)

            bill = {
                "branch":branch.name,
                "transaction_miti":str(transaction_miti),
                "agent":None,
                "agent_name":'',
                "terminal":1,
                "customer_name":student.name,
                "customer_address":student.address,
                "customer_tax_number":'',
                "customer":student.id,
                "transaction_date_time": str(transaction_date_time),
                "transaction_date":str(transaction_date),
                "sub_total":sub_total,
                "discount_amount":discount_amount,
                "taxable_amount":taxable_amount,
                "tax_amount":tax_amount,
                "grand_total":grand_total,
                "service_charge":0.0,
                "amount_in_words":amount_in_words,
                "organization":Organization.objects.last().org_name if Organization.objects.last() else None,
                "print_count":1,
                "payment_mode":'Credit',
                "month":month,
                "year":year,
                "bill_items": []
            }

            bill["bill_items"] = bill_items
        return Response({"bills" : bill},status=200)
