from rest_framework.viewsets import ModelViewSet

from user.models import Customer

from canteen.models import StudentAttendance

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAuthenticated

from api.serializers.canteen import StudentAttendanceSerializer
from canteen.models import tblmissedattendance_butcharged

class StudentAttendanceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StudentAttendance.objects.filter(is_deleted=False, status=True)
    serializer_class = StudentAttendanceSerializer
    
    def destroy(self, request, *args, **kwargs):
        student_attendance = self.get_object()
        
        # Check if the attendance record is associated with a bill
        if student_attendance.bill_created:
            return Response(
                {"detail": "Cannot delete attendance because a bill exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the noeatbutcharged flag from request data
        noeatbutcharged = request.data.get('noeatbutcharged', False)
        
        # Get student and date info
        student = student_attendance.student
        date = student_attendance.eaten_date
        day_of_week = date.strftime("%A")
        
        # Get appropriate product based on day and meal preference
        if day_of_week == "Wednesday":
            if student.meal_preference == "nonveg":
                product = Product.objects.filter(
                    is_canteen_item=True, 
                    lunch_type="nonveg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
            else:
                product = Product.objects.filter(
                    is_canteen_item=True, 
                    lunch_type="veg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
        elif day_of_week == "Friday":
            if student.meal_preference in ["egg", "nonveg"]:
                product = Product.objects.filter(
                    is_canteen_item=True, 
                    lunch_type="egg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
            else:
                product = Product.objects.filter(
                    is_canteen_item=True, 
                    lunch_type="veg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
        else:
            product = Product.objects.filter(
                is_canteen_item=True, 
                lunch_type="veg",
                min_class__lte=student.student_class,
                max_class__gte=student.student_class
            ).first()
        
        if not product:
            return Response(
                {"detail": "Could not find appropriate product for this student."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create record based on the flag
        if noeatbutcharged:
            # Create record in tblmissedattendance_butcharged
            tblmissedattendance_butcharged.objects.create(
                student=student,
                Lunchtype=student.meal_preference,
                missed_date=date,
                product=product,
                rate=product.price
            )
            message = "Attendance deleted and marked as missed but charged"
        else:
            # Create record in tblmissedattendance
            tblmissedattendance.objects.create(
                student=student,
                Lunchtype=student.meal_preference,
                missed_date=date,
                day=day_of_week,
                pre_informed=False,
                product=product
            )
            message = "Attendance deleted and marked as missed (not charged)"
        
        # Perform the deletion
        self.perform_destroy(student_attendance)
        
        # Return success response
        return Response(
            {
                "status": "success",
                "message": message,
                "deleted_attendance_id": student_attendance.id,
                "student_id": student.id,
                "date": date
            },
            status=status.HTTP_200_OK
    )



from rest_framework.response import Response
from django.db import transaction
from datetime import datetime
from canteen.utils import check_studentattendance_forleave
from canteen.models import tblmissedattendance
from canteen.models import WorkingDays

class StudentAttendanceListCreate(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        json_data = request.data
        # data = request.data

        data = json_data.get('present', None)

        absent_data = json_data.get('absent', None)


        # Ensure the data is always a list
        if isinstance(data, dict):  
            data = [data]
        if data != []:
            student_class = data[0]["class"]   
        
        for entry in data:
            # Check if the attendance entry for the student already exists for the given date
            student_id = entry.get("student")
            eaten_date = entry.get("eaten_date")

            # Check if an attendance record already exists for this student and eaten_date
            existing_entry = StudentAttendance.objects.filter(student=student_id, eaten_date=eaten_date).first()
                
            if existing_entry:
                return Response(
                        {"error": f"Attendance for student {existing_entry.student.name} on {eaten_date} already exists."},
                        status=400
                )
            
            else:
                tblmissedattendance_obj = tblmissedattendance.objects.filter(student__id = student_id, missed_date=eaten_date).first()
                if tblmissedattendance_obj:
                    tblmissedattendance_obj.delete()
                tblmissedattendance_butcharged_obj = tblmissedattendance_butcharged.objects.filter(student__id = student_id, missed_date=eaten_date).first()
                if tblmissedattendance_butcharged_obj:
                    tblmissedattendance_butcharged_obj.delete()
                    
                # Now check future working days (next 2) to see if this attendance affects any missed records
                try:
                    eaten_date_obj = datetime.strptime(eaten_date, "%Y-%m-%d").date()
                    
                    # Get next 2 working days after the eaten_date
                    next_working_days = WorkingDays.objects.filter(
                        working_date__gt=eaten_date_obj
                    ).order_by('working_date')[:2]
                    
                    print(next_working_days)
                    for working_day in next_working_days:

                        tblmissedobj = tblmissedattendance.objects.filter(
                            student__id=student_id,
                            missed_date=working_day.working_date
                        ).first()
                        
                        if tblmissedobj:
                            # student_obj = Customer.objects.get(id=student_id)
                            tblmissedattendance_butcharged.objects.create(
                                student=tblmissedobj.student,
                                missed_date=working_day.working_date,
                                Lunchtype=tblmissedobj.Lunchtype,
                                rate=tblmissedobj.product.price,
                                product = tblmissedobj.product
                            )     
                            
    
                            tblmissedobj.delete()
                        
                except Exception as e:
                    print(f"Error processing future working days: {str(e)}")


        for datum in data:
            eaten_date_str = datum.get("eaten_date")

            # Convert eaten_date string to day of the week
            today_day = datetime.strptime(eaten_date_str, "%Y-%m-%d").strftime("%A")
            student = Customer.objects.filter(id=datum["student"]).first()
            nonveg_canteen_product = Product.objects.filter(is_canteen_item=True, lunch_type="nonveg", min_class__lte=student.student_class, max_class__gte=student.student_class).first()
            nonveg_product_rate = nonveg_canteen_product.price if nonveg_canteen_product else 0.0

            veg_canteen_product = Product.objects.filter(is_canteen_item=True, lunch_type="veg", min_class__lte=student.student_class, max_class__gte=student.student_class).first()
            veg_product_rate = veg_canteen_product.price if veg_canteen_product else 0.0

            egg_canteen_product = Product.objects.filter(is_canteen_item=True, lunch_type="egg", min_class__lte=student.student_class, max_class__gte=student.student_class).first()
            egg_product_rate = egg_canteen_product.price if egg_canteen_product else 0.0
            if today_day == "Wednesday":   
                if student:
                    student_meal_preference = student.meal_preference

                    if student_meal_preference == "nonveg":

                        nonveg_product_rate = nonveg_canteen_product.price if nonveg_canteen_product else 0.0
                        datum["product"] = nonveg_canteen_product.id
                        datum["rate"] = nonveg_product_rate
                        datum["total"] = nonveg_product_rate
                    else:
                        datum["product"] = veg_canteen_product.id
                        datum["rate"] = veg_product_rate
                        datum["total"] = veg_product_rate
                else:
                    print("Student id came null for wednesday meal preference")

            elif today_day == "Friday":
                if student:
                    student_meal_preference = student.meal_preference
                    if student_meal_preference == "egg" or student_meal_preference == "nonveg":
                        datum["product"] = egg_canteen_product.id
                        datum["rate"] = egg_product_rate
                        datum["total"] = egg_product_rate
                    else:
                        datum["product"] = veg_canteen_product.id
                        datum["rate"] = veg_product_rate
                        datum["total"] = veg_product_rate  
                else:
                    print("Student id came null for friday meal preference")
            else:
                datum["product"] = veg_canteen_product.id
                datum["rate"] = veg_product_rate
                datum["total"] = veg_product_rate                            
        serializer = StudentAttendanceSerializer(data=data, many=True)
        print(data)

        check_studentattendance_forleave(absent_data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Student canteen attendance created successfully"}, status=200)
            # else:
            #     return Response({"error": f"Data is not valid "}, status=400)
        except Exception as e:
            print(str(e))
            return Response({"error": f"Data is not valid "}, status=400)

class DatewiseStudentAttendanceList(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):

        data = request.data
        # Ensure the data is always a list
        date = data["date"]
        studentattendance_data = StudentAttendance.objects.filter(eaten_date=date)
        serializer = StudentAttendanceSerializer(studentattendance_data, many=True)

        return Response(serializer.data, 200)
    
from datetime import datetime
from django.db.models import Count, Sum
class DatewiseStudentAggregateAttendanceList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        data = request.data

        # Extract 'from_date' and 'to_date' from request data
        from_date = data["from_date"]
        to_date = data["to_date"]
        
        student_id = data.get("student_id", None)


        # Ensure date format is correct (optional, depends on your input format)
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        if student_id:
            # Query with date range filter
            meal_eatens_by_students = (
                StudentAttendance.objects
                .filter(eaten_date__range=[from_date, to_date], student__id=int(student_id))  # Date range filter
                .values('student', 'student__name', 'student__student_class','student__roll_no', 'student__section', 'rate', 'total' )  
                .annotate(no_of_entries=Count('id'))  
                .order_by('-no_of_entries')  
            )
        meal_eatens_by_students = (
            StudentAttendance.objects
            .filter(status=True, is_deleted=False, bill_created=False, eaten_date__range=[from_date, to_date])
            .values('student', 'student__name', 'student__student_class', 'student__roll_no', 'student__section')
            .annotate(no_of_entries=Count('id'), total_sum=Sum('total'))
            .order_by('-no_of_entries')
        )

        studentAttendanceIndividualData = StudentAttendance.objects.filter(eaten_date__range=[from_date, to_date])
        serializer = StudentAttendanceSerializer(studentAttendanceIndividualData, many=True)
        # Convert QuerySet to list for JSON response
        individualDataList = serializer.data
        response_data = list(meal_eatens_by_students)

        for item in individualDataList:
            item["rate"] = float(item["rate"])
            item["total"] = float(item["total"])

        missed_charged_data = (
            tblmissedattendance_butcharged.objects
            .filter(status=True, is_deleted=False, missed_date__range=[from_date, to_date])
            .values(
                'id',
                'student_id',
                'student__name',
                'Lunchtype',
                'rate',
                'product_id',
                'product__title',
                'missed_date'
            )
        )

        if not response_data:
            return Response({"message": "No attendance records found for the given date range."}, status=200)
        return Response({"aggregated_data" :response_data, "individual_data": individualDataList,"missedattendance_charged": list(missed_charged_data)}, status=200)


from canteen.utils import create_student_bills
class TestCronjob(APIView):
    def get(self, request):
        try:
            create_student_bills()
            return Response("Bill created successfully", 200)
        except Exception as e:
            return Response(str(e), 400)

import nepali_datetime
from product.models import Product
from canteen.utils import convert_amount_to_words
from bill.models import Bill, BillItem
from organization.models import Branch, Organization
import pytz
from bill.utils import product_sold
from django.db import transaction

from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import pytz
from datetime import datetime
import nepali_datetime

class CheckoutCanteenBill(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            student_id = int(data.get("student_id", None))
        except (TypeError, ValueError):
            return Response({
                "success": False,
                "message": "Invalid or missing student_id"
            }, status=status.HTTP_400_BAD_REQUEST)

        nepal_tz = pytz.timezone("Asia/Kathmandu")
        transaction_datetime = datetime.now(nepal_tz)
        transaction_date_time = transaction_datetime.strftime("%Y-%m-%d %H:%M:%S")
        transaction_date = transaction_datetime.strftime("%Y-%m-%d")

        student = Customer.objects.filter(id=student_id).first()
        if not student:
            return Response({
                "success": False,
                "message": f"Student with ID {student_id} not found!"
            }, status=status.HTTP_404_NOT_FOUND)

        attendances = (
            StudentAttendance.objects
            .filter(student=student, bill_created=False)
            .values('product', 'rate')
            .annotate(no_of_entries=Count('id'))
        )

        if not attendances:
            return Response({
                "success": False,
                "message": f"No pending attendance records found for {student.name}."
            }, status=status.HTTP_400_BAD_REQUEST)

        branch = Branch.objects.active().filter(is_central_billing=True).last()
        if not branch:
            return Response({
                "success": False,
                "message": "No active central billing branch found!"
            }, status=status.HTTP_400_BAD_REQUEST)

        bill_items = []
        sub_total = 0

        for att in attendances:
            product = Product.objects.filter(id=att['product']).first()
            if not product:
                continue
            quantity = att['no_of_entries']
            rate = float(att['rate'])
            amount = quantity * rate
            sub_total += amount

            bill_item = BillItem.objects.create(
                product_quantity=quantity,
                rate=rate,
                product_title=product.title,
                unit_title=product.unit,
                amount=amount,
                product=product
            )
            product_sold(bill_item)
            bill_items.append(bill_item)

        tax_amount = sub_total * 0.13
        taxable_amount = sub_total
        grand_total = sub_total + tax_amount
        amount_in_words = convert_amount_to_words(grand_total)

        nepali_today = nepali_datetime.date.today()

        bill = Bill.objects.create(
            branch=branch,
            transaction_miti=nepali_today,
            agent=None,
            agent_name='',
            terminal=1,
            customer_name=student.name,
            customer_address=student.address,
            customer_tax_number='',
            customer=student,
            transaction_date_time=transaction_date_time,
            transaction_date=transaction_date,
            sub_total=sub_total,
            discount_amount=0.0,
            taxable_amount=taxable_amount,
            tax_amount=tax_amount,
            grand_total=grand_total,
            service_charge=0.0,
            amount_in_words=amount_in_words,
            organization=Organization.objects.last(),
            print_count=1,
            payment_mode='Credit'
        )

        bill.bill_items.add(*bill_items)

        # Mark those attendance records as billed
        StudentAttendance.objects.filter(student=student, bill_created=False).update(bill_created=True)

        return Response({
            "bill_id": bill.id,
            "success": True,
            "message": f"Bill created successfully for {student.name}"
        }, status=status.HTTP_200_OK)
        
from canteen.utils import create_student_bills_for_class, create_advance_bills_for_class
class CheckoutClassBills(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        data = request.data

        student_class = data.get("class", None)

        if student_class:
            try:
                # create_student_bills_for_class(student_class)
                result = create_advance_bills_for_class(student_class)
                # return Response({"data": f"Bills created for class {student_class}"}, 200)
                if result['success']:
                    return Response({"data": result['message']}, status=200)
                else:
                    return Response({"error": result['message']}, status=400)
            except Exception as e:
                print(f"Error in creating bill for class {student_class} with {e}")
                return Response({"error": f"Error in creating bills for class {student_class}", }, 400)
        else:
            print("Student class cannot be none")
            return Response({"error": "No class provided"}, 400)

from rest_framework.response import Response
from rest_framework import status
import jwt
from user.models import User
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class VerifyToken(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        
        # Get token from query parameter instead of headers
        token = request.GET.get('token')

        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=int(payload['user_id']))

            # Return user details
            return Response({'valid': True})

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

from user.models import Customer
from canteen.models import PreInformedLeave

class StudentsServedData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from datetime import datetime
        from django.utils import timezone
        from django.db.models import Count, Q

        now = timezone.now()

        try:
            # Define class groups
            class_groups = {
                '1-5': (1, 5),
                '6-10': (6, 10),
                '11-12': (11, 12)
            }

            # Initialize response structure
            response_data = {
                "today": {},
                "month": {}
            }

            # Process each class group
            for group_name, (start_class, end_class) in class_groups.items():
                # Total students in this group
                total_in_group = Customer.objects.filter(
                    student_class__gte=start_class,
                    student_class__lte=end_class,
                    status=True,
                    is_deleted=False
                ).count()

                # Today's data for this group
                students_served_today = StudentAttendance.objects.filter(
                    student__student_class__gte=start_class,
                    student__student_class__lte=end_class,
                    eaten_date=now.date(),
                    status=True,
                    is_deleted=False
                ).count()

                on_leave_today = PreInformedLeave.objects.filter(
                    student__student_class__gte=start_class,
                    student__student_class__lte=end_class,
                    start_date__lte=now.date(),
                    end_date__gte=now.date()
                ).count()

                # Monthly data for this group
                students_served_month = StudentAttendance.objects.filter(
                    student__student_class__gte=start_class,
                    student__student_class__lte=end_class,
                    eaten_date__year=now.year,
                    eaten_date__month=now.month,
                    status=True,
                    is_deleted=False
                ).count()

                # Add to response
                response_data["today"][group_name] = {
                    "total_no_students": total_in_group,
                    "total_students_served": students_served_today,
                    "total_no_of_students_to_serve": total_in_group - on_leave_today
                }

                response_data["month"][group_name] = {
                    "total_no_students": total_in_group,
                    "total_students_served": students_served_month
                }

            # Add overall totals
            overall_total = Customer.objects.filter(
                student_class__isnull=False,
                status=True,
                is_deleted=False
            ).count()

            overall_served_today = StudentAttendance.objects.filter(
                eaten_date=now.date(),
                status=True,
                is_deleted=False
            ).count()

            overall_on_leave = PreInformedLeave.objects.filter(
                start_date__lte=now.date(),
                end_date__gte=now.date()
            ).count()

            overall_served_month = StudentAttendance.objects.filter(
                eaten_date__year=now.year,
                eaten_date__month=now.month,
                status=True,
                is_deleted=False
            ).count()

            response_data["today"]["overall"] = {
                "total_no_students": overall_total,
                "total_students_served": overall_served_today,
                "total_no_of_students_to_serve": overall_total - overall_on_leave
            }

            response_data["month"]["overall"] = {
                "total_no_students": overall_total,
                "total_students_served": overall_served_month
            }

            return Response(response_data, 200)

        except Exception as e:
            return Response({"error": str(e)}, 400)


from canteen.utils import create_advance_bills_for_class_by_month


class CheckoutClassBillsByMonth(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        student_class = data.get("class", None)
        month = data.get("month", None)
        year = data.get("year", None)

        if not all([student_class, month, year]):
            return Response({"error": "Class, month and year are required"}, status=400)

        try:
            month = int(month)
            year = int(year)
            
            # Optional: Add validation for month/year ranges
            if month < 1 or month > 12:
                return Response({"error": "Month must be between 1 and 12"}, status=400)
            result = create_advance_bills_for_class_by_month(student_class, month, year)
            if result['success']:
                return Response({"data": result['message']}, status=200)
            else:
                return Response({"error": result['message']}, status=400)
        except Exception as e:
            print(f"Error in creating bill for class {student_class} with {e}")
            return Response({"error": f"Error in creating bills for class {student_class}"}, status=400)
            
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.db.models import Q
from canteen.models import StudentAttendance, tblmissedattendance, tblmissedattendance_butcharged
from user.models import Customer

class MonthlyAttendanceReportAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        student_id = request.query_params.get('student_id')  # Get student_id from query params
        
        if not month or not year:
            return Response(
                {"error": "Both month and year parameters are required"},
                status=400
            )
        
        try:
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise ValueError
            if student_id:
                student_id = int(student_id)  # Convert to int if provided
        except ValueError:
            return Response(
                {"error": "Invalid parameters. Month must be 1-12, year and student_id must be integers"},
                status=400
            )
        
        # Calculate date range for the month
        if month == 12:
            month_end = datetime(year+1, 1, 1).date()
        else:
            month_end = datetime(year, month+1, 1).date()
        month_start = datetime(year, month, 1).date()
        
        # Base querysets with date filtering
        student_qs = StudentAttendance.objects.filter(
            eaten_date__gte=month_start,
            eaten_date__lt=month_end
        )
        missed_qs = tblmissedattendance.objects.filter(
            missed_date__gte=month_start,
            missed_date__lt=month_end
        )
        charged_qs = tblmissedattendance_butcharged.objects.filter(
            missed_date__gte=month_start,
            missed_date__lt=month_end
        )
        
        # Add student filter if student_id is provided
        if student_id:
            student_qs = student_qs.filter(student_id=student_id)
            missed_qs = missed_qs.filter(student_id=student_id)
            charged_qs = charged_qs.filter(student_id=student_id)
        
        # Execute queries with select_related
        student_attendances = student_qs.select_related('student', 'product')
        missed_attendances = missed_qs.select_related('student', 'product')
        but_charged_attendances = charged_qs.select_related('student', 'product')
        
        # Prepare response data
        response_data = {
            "month": month,
            "year": year,
            "student_id": student_id,
            "student_attendances": [],
            "missed_attendances": [],
            "but_charged_attendances": []
        }
        
        # Process student attendances
        for attendance in student_attendances:
            response_data["student_attendances"].append({
                "id": attendance.id,
                "student": {
                    "id": attendance.student.id,
                    "name": attendance.student.name,
                    "class": attendance.student.student_class,
                    "section": attendance.student.section
                },
                "date": attendance.eaten_date,
                "day": attendance.eaten_date.strftime("%A"),
                "product": attendance.product.title if attendance.product else None,
                "rate": float(attendance.rate),
                "total": float(attendance.total),
                "bill_created": attendance.bill_created
            })
        
        # Process missed attendances
        for missed in missed_attendances:
            response_data["missed_attendances"].append({
                "id": missed.id,
                "student": {
                    "id": missed.student.id,
                    "name": missed.student.name,
                    "class": missed.student.student_class,
                    "section": missed.student.section
                },
                "date": missed.missed_date,
                "day": missed.day,
                "product": missed.product.title if missed.product else None,
                "lunch_type": missed.Lunchtype,
                "pre_informed": missed.pre_informed,
                "considered_next_month": missed.considered_next_month
            })
        
        # Process but-charged attendances
        for charged in but_charged_attendances:
            response_data["but_charged_attendances"].append({
                "id": charged.id,
                "student": {
                    "id": charged.student.id,
                    "name": charged.student.name,
                    "class": charged.student.student_class,
                    "section": charged.student.section
                },
                "date": charged.missed_date,
                "product": charged.product.title if charged.product else None,
                "lunch_type": charged.Lunchtype,
                "rate": float(charged.rate)
            })
        
        return Response(response_data)
        
class ChangeNotChargedtoCharged(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        missedattendance_id = data["missedattendance_id"]

        missedattendance = tblmissedattendance.objects.get(id=int(missedattendance_id))

        if not missedattendance:
            return Response({"error": "No missed attendance found"}, 400)

        student = missedattendance.student
        Lunchtype = missedattendance.Lunchtype
        missed_date = missedattendance.missed_date
        product = missedattendance.product    

        tblmissedattendance_butcharged.objects.create(
            student=student,
            Lunchtype=Lunchtype,
            missed_date=missed_date,
            product=product,
            rate=product.price
        )     

        missedattendance.delete()


        return Response({"data":"Changed Credit date to charged successfully"}, 200)
    

from datetime import datetime
import calendar

class ChangeChargedtoNoCharged(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        missedattendance_butcharged_id = data["missedattendance_id"]

        missedattendance_butcharged = tblmissedattendance_butcharged.objects.get(id=int(missedattendance_butcharged_id))

        if not missedattendance_butcharged:
            return Response({"error": "No charged missed attendance found"}, 400)

        student = missedattendance_butcharged.student
        Lunchtype = missedattendance_butcharged.Lunchtype
        missed_date = missedattendance_butcharged.missed_date
        product = missedattendance_butcharged.product

        # Extract day from missed_date
        if isinstance(missed_date, str):
            missed_date = datetime.strptime(missed_date, "%Y-%m-%d").date()
        day = calendar.day_name[missed_date.weekday()]  # e.g., "Monday"

        # Create new tblmissedattendance
        tblmissedattendance.objects.create(
            student=student,
            Lunchtype=Lunchtype,
            missed_date=missed_date,
            product=product,
            day=day,
            pre_informed=False
        )

        missedattendance_butcharged.delete()

        return Response({"data": "Changed charged date to Credit successfully"}, 200)