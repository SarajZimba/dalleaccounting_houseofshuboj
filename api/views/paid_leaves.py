from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.paid_leaves import tblcompanypaidleavePolicySerializer
from employee.models import tblcompanypaidleavePolicy, tblleaveapply
from datetime import datetime

class tblcompanypaidleavePolicyCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            policy = tblcompanypaidleavePolicy.objects.first()  # Get the first (and only) policy
            if not policy:
                return Response({"detail": "No policy found."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = tblcompanypaidleavePolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            policy = tblcompanypaidleavePolicy.objects.first()  # Check for an existing policy
            if policy:
                # Update the existing policy
                serializer = tblcompanypaidleavePolicySerializer(policy, data=request.data, partial=True)
            else:
                # Create a new policy if none exists
                serializer = tblcompanypaidleavePolicySerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK if policy else status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# from employee.models import Employee

# from employee.models import tblpaidleaves
# class tblleaveapplyCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         # Get empID from the request
#         empID = data.get("empID")
#         if empID is None:
#             return Response({"error": "No employee selected"}, status=400)

#         # Fetch employee instance
#         try:
#             employee = Employee.objects.get(id=int(empID))
#         except Employee.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=404)


#         # Get leave dates and reason
#         leave_date_from = data.get("leave_date_from")
#         leave_date_to = data.get("leave_date_to")
#         reason = data.get("reason", None)

#         if not leave_date_from or not leave_date_to:
#             return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)

#         # Convert leave dates to date objects
#         try:
#             leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
#             leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#         # Calculate noOfDays (inclusive difference)
#         no_of_days = (leave_date_to - leave_date_from).days + 1
#         if no_of_days <= 0:
#             return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

#         # Fetch the no of paid leaves 
#         employees_paid_leaves_data = tblpaidleaves.objects.get(empID= employee)

#         if employees_paid_leaves_data.no_of_leaves < no_of_days:
#             holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
#             employees_paid_leaves_data.no_of_leaves = 0
#             employees_paid_leaves_data.save()
#             difference_for_unpaid_leaves_for_tblleaveapply = no_of_days - holder_for_employees_previous_paid_leaves
#             difference_for_paid_leaves_for_tblleaveapply = holder_for_employees_previous_paid_leaves

#         else:
#             holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
#             difference_for_paid_leaves_for_tblleaveapply = holder_for_employees_previous_paid_leaves - no_of_days
#             difference_for_unpaid_leaves_for_tblleaveapply = 0
#             employees_paid_leaves_data.no_of_leaves = difference_for_paid_leaves_for_tblleaveapply
#             employees_paid_leaves_data.save()



#         # Set applyDate to today's date
#         apply_date = datetime.today().date()

#         # Create tblleaveapply object
#         leave_apply = tblleaveapply.objects.create(
#             empID=employee,
#             applyDate=apply_date,
#             noOfDays=no_of_days,
#             leaveDateFrom=leave_date_from,
#             leaveDateTo=leave_date_to,
#             reason=reason,
#             noOfPaidLeaves = difference_for_paid_leaves_for_tblleaveapply,
#             noOfUnPaidLeaves = difference_for_unpaid_leaves_for_tblleaveapply

#         )

#         # Serialize and return the created object (if needed)
#         response_data = {
#             "id": leave_apply.id,
#             "empID": leave_apply.empID.id,
#             "applyDate": leave_apply.applyDate,
#             "noOfDays": leave_apply.noOfDays,
#             "leaveDateFrom": leave_apply.leaveDateFrom,
#             "leaveDateTo": leave_apply.leaveDateTo,
#             "reason": leave_apply.reason,
#             "noOfPaidLeaves": leave_apply.noOfPaidLeaves,
#             "noofUnPaidLeaves": leave_apply.noOfUnPaidLeaves,
#         }

#         return Response(response_data, status=status.HTTP_201_CREATED)  

from employee.models import Employee
import nepali_datetime
from datetime import timedelta

from employee.utils import convert_eng_to_nepali
from employee.models import tblpaidleaves
import json

class tblleaveapplyCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        # Get empID from the request
        empID = data.get("empID")
        if empID is None:
            return Response({"error": "No employee selected"}, status=400)

        # Fetch employee instance
        try:
            employee = Employee.objects.get(id=int(empID))
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)


        # Get leave dates and reason
        leave_date_from = data.get("leave_date_from")
        leave_date_to = data.get("leave_date_to")
        reason = data.get("reason", None)



        if not leave_date_from or not leave_date_to:
            return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)


        nepali_year, converted_nepali_date = convert_eng_to_nepali(leave_date_from)
        # Convert leave dates to date objects
        try:
            leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
            leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        from employee.models import DailyAttendance        
        if DailyAttendance.objects.filter(attendance_date__range=(leave_date_from, leave_date_to), empID=employee).exists():
            return Response({"error": "Employee cannot take leave from today cause they are already cheked in"})

        # Calculate noOfDays (inclusive difference)
        no_of_days = (leave_date_to - leave_date_from).days + 1
        if no_of_days <= 0:
            return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

        # Fetch the no of paid leaves 
        employees_paid_leaves_data = tblpaidleaves.objects.get(empID= employee)
        no_of_paidleaves_taken = 0.0

        if employees_paid_leaves_data.no_of_leaves < no_of_days:
            holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
            employees_paid_leaves_data.no_of_leaves = 0
            employees_paid_leaves_data.save()
            difference_for_unpaid_leaves_for_tblleaveapply = no_of_days - holder_for_employees_previous_paid_leaves
            difference_for_paid_leaves_for_tblleaveapply = 0.0
            no_of_paidleaves_taken = holder_for_employees_previous_paid_leaves


        else:
            holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
            difference_for_paid_leaves_for_tblleaveapply = holder_for_employees_previous_paid_leaves - no_of_days
            difference_for_unpaid_leaves_for_tblleaveapply = 0
            employees_paid_leaves_data.no_of_leaves = difference_for_paid_leaves_for_tblleaveapply
            no_of_paidleaves_taken = no_of_days

            employees_paid_leaves_data.save()

        # Convert English dates to Nepali months and count leave days per month
        nepali_month_count = {}
        current_date = leave_date_from

        while current_date <= leave_date_to:
            nepali_date = nepali_datetime.date.from_datetime_date(current_date)
            nepali_month = nepali_date.strftime("%B")  # Get Nepali month name
            
            if nepali_month in nepali_month_count:
                nepali_month_count[nepali_month] += 1
            else:
                nepali_month_count[nepali_month] = 1

            current_date += timedelta(days=1)

        # Store as a JSON string in the database
        nepali_month_json = json.dumps(nepali_month_count)

        # Set applyDate to today's date
        apply_date = datetime.today().date()

        # Create tblleaveapply object
        leave_apply = tblleaveapply.objects.create(
            empID=employee,
            applyDate=apply_date,
            noOfDays=no_of_days,
            leaveDateFrom=leave_date_from,
            leaveDateTo=leave_date_to,
            reason=reason,
            noOfPaidLeaves = difference_for_paid_leaves_for_tblleaveapply,
            noOfUnPaidLeaves = difference_for_unpaid_leaves_for_tblleaveapply,
            nepali_month=nepali_month_json,  # Store as JSON string
            nepali_year = nepali_year,
            nepali_date = converted_nepali_date,
            noOfPaidLeaves_taken= no_of_paidleaves_taken

        )

        # Serialize and return the created object (if needed)
        response_data = {
            "id": leave_apply.id,
            "empID": leave_apply.empID.id,
            "applyDate": leave_apply.applyDate,
            "noOfDays": leave_apply.noOfDays,
            "leaveDateFrom": leave_apply.leaveDateFrom,
            "leaveDateTo": leave_apply.leaveDateTo,
            "reason": leave_apply.reason,
            "noOfPaidLeaves": leave_apply.noOfPaidLeaves,
            "noofUnPaidLeaves": leave_apply.noOfUnPaidLeaves,
        }

        return Response(response_data, status=status.HTTP_201_CREATED) 

        
from employee.models import tblpaidleaves
class GetEmploeeNoofPaidLeavesApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        employee = data.get("emp_ID", None)

        try:
            employee = Employee.objects.get(id=int(employee))

        except Exception as e:
            return Response({"error": "No employee found"}, 400)
        
        employee_paidleaves = tblpaidleaves.objects.get(empID=employee)

        no_of_days = employee_paidleaves.no_of_leaves

        return Response({"paidleaves": no_of_days}, 200)
        

from api.serializers.paid_leaves import tblleaveapplySerializer
from employee.models import tblpaidleaves
class tblleaveapplyListAPIView(APIView):
    def get(self, request, *args, **kwargs):

        # Create tblleaveapply object
        pending_leave_apply = tblleaveapply.objects.filter(current_status=None,  empID__current_status="Enrolled")
        approved_leave_apply = tblleaveapply.objects.filter(current_status="Approved",  empID__current_status="Enrolled")
        cancelled_leave_apply = tblleaveapply.objects.filter(current_status="Cancelled",  empID__current_status="Enrolled")

        # Serialize and return the created object (if needed)

        pending_leave_serializer = tblleaveapplySerializer(pending_leave_apply, many=True)
        approved_leave_serializer = tblleaveapplySerializer(approved_leave_apply, many=True)
        cancelled_leave_serializer = tblleaveapplySerializer(cancelled_leave_apply, many=True)

        response_data = {"pending_leave": pending_leave_serializer.data, "approved_leave": approved_leave_serializer.data, "cancelled_leave": cancelled_leave_serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)  

        
from employee.models import tblpaidleaves
class confirmleaveapplyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        

        data = request.data

        tblleaveapply_id = data["id"]
        tblleaveapply_obj = tblleaveapply.objects.get(id=int(tblleaveapply_id))
        # Create tblleaveapply object


        tblleaveapply_obj.current_status = "Approved"

        tblleaveapply_obj.save()
        # Serialize and return the created object (if needed)

        return Response({"leave has been approved"}, status=status.HTTP_201_CREATED)  
        
class tblleaveapplyUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        # Get empID from the request
        empID = data.get("empID")
        if empID is None:
            return Response({"error": "No employee selected"}, status=400)

        # Fetch employee instance
        try:
            employee = Employee.objects.get(id=int(empID))
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)


        # Get leave dates and reason
        leave_date_from = data.get("leave_date_from")
        leave_date_to = data.get("leave_date_to")
        reason = data.get("reason", None)
        tblleaveapply_id  = data.get("id", None)
        current_status = data.get("current_status", None)

        if not leave_date_from or not leave_date_to:
            return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)
        # Convert leave dates to date objects
        try:
            leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
            leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
            
        from employee.models import DailyAttendance        
        if DailyAttendance.objects.filter(attendance_date__range=(leave_date_from, leave_date_to), empID=employee).exists():
            return Response({"error": "Employee cannot take leave from today cause they are already cheked in"})

        try:
            tblleaveapply_obj = tblleaveapply.objects.get(id=int(tblleaveapply_id))
        except Exception as e:
            return Response({"error": "No leave apply found of that id"}, 400)
        applyDate = tblleaveapply_obj.applyDate


        noOfPaidLeaves_taken = tblleaveapply_obj.noOfPaidLeaves_taken

        if noOfPaidLeaves_taken != 0.0:
            employee_tblpaidleaves_obj = tblpaidleaves.objects.get(empID__id = int(empID))
            employee_tblpaidleaves_obj.no_of_leaves += noOfPaidLeaves_taken
            employee_tblpaidleaves_obj.save()
        if current_status == "Cancelled":
            tblleaveapply_obj.current_status = "Cancelled"
            tblleaveapply_obj.save()
            return Response({"detail": "Leave cancelled successfully"}, status=status.HTTP_201_CREATED) 
        tblleaveapply_obj.delete()


        # Convert back to string in the same format
        leave_date_from_str = leave_date_from.strftime("%Y-%m-%d")
        leave_date_to_str = leave_date_to.strftime("%Y-%m-%d")
        nepali_year, converted_nepali_date = convert_eng_to_nepali(leave_date_from_str)


        # Calculate noOfDays (inclusive difference)
        no_of_days = (leave_date_to - leave_date_from).days + 1
        if no_of_days <= 0:
            return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

        # Fetch the no of paid leaves 
        employees_paid_leaves_data = tblpaidleaves.objects.get(empID= employee)
        no_of_paidleaves_taken = 0.0
        if employees_paid_leaves_data.no_of_leaves < no_of_days:
            holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
            employees_paid_leaves_data.no_of_leaves = 0
            employees_paid_leaves_data.save()
            difference_for_unpaid_leaves_for_tblleaveapply = no_of_days - holder_for_employees_previous_paid_leaves
            difference_for_paid_leaves_for_tblleaveapply = 0
            no_of_paidleaves_taken = holder_for_employees_previous_paid_leaves
        else:
            holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
            difference_for_paid_leaves_for_tblleaveapply = holder_for_employees_previous_paid_leaves - no_of_days
            difference_for_unpaid_leaves_for_tblleaveapply = 0
            employees_paid_leaves_data.no_of_leaves = difference_for_paid_leaves_for_tblleaveapply
            no_of_paidleaves_taken = no_of_days
            employees_paid_leaves_data.save()

        # Convert English dates to Nepali months and count leave days per month
        nepali_month_count = {}
        current_date = leave_date_from

        while current_date <= leave_date_to:
            nepali_date = nepali_datetime.date.from_datetime_date(current_date)
            nepali_month = nepali_date.strftime("%B")  # Get Nepali month name
            
            if nepali_month in nepali_month_count:
                nepali_month_count[nepali_month] += 1
            else:
                nepali_month_count[nepali_month] = 1

            current_date += timedelta(days=1)

        # Store as a JSON string in the database
        nepali_month_json = json.dumps(nepali_month_count)

        # # Set applyDate to today's date
        # apply_date = datetime.today().date()
        if current_status == "Pending" or current_status == "":
            current_status = None
        # Create tblleaveapply object
        leave_apply = tblleaveapply.objects.create(
            empID=employee,
            applyDate=applyDate,
            noOfDays=no_of_days,
            leaveDateFrom=leave_date_from,
            leaveDateTo=leave_date_to,
            reason=reason,
            noOfPaidLeaves = difference_for_paid_leaves_for_tblleaveapply,
            noOfUnPaidLeaves = difference_for_unpaid_leaves_for_tblleaveapply,
            nepali_month=nepali_month_json,  # Store as JSON string
            nepali_year = nepali_year,
            nepali_date = converted_nepali_date,
            current_status=current_status,
            noOfPaidLeaves_taken= no_of_paidleaves_taken
        )

        # Serialize and return the created object (if needed)
        response_data = {
            "id": leave_apply.id,
            "empID": leave_apply.empID.id,
            "applyDate": leave_apply.applyDate,
            "noOfDays": leave_apply.noOfDays,
            "leaveDateFrom": leave_apply.leaveDateFrom,
            "leaveDateTo": leave_apply.leaveDateTo,
            "reason": leave_apply.reason,
            "noOfPaidLeaves": leave_apply.noOfPaidLeaves,
            "noofUnPaidLeaves": leave_apply.noOfUnPaidLeaves,
        }

        return Response(response_data, status=status.HTTP_201_CREATED) 
        
class tblleaveapplyCancelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        # Get empID from the request
        empID = data.get("empID")
        if empID is None:
            return Response({"error": "No employee selected"}, status=400)

        # Fetch employee instance
        try:
            employee = Employee.objects.get(id=int(empID))
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        tblleaveapply_id  = data.get("id", None)
        try:
            tblleaveapply_obj = tblleaveapply.objects.get(id=int(tblleaveapply_id))
        except Exception as e:
            return Response({"error": "No leave apply found of that id"}, 400)
        if tblleaveapply_obj.current_status == "Cancelled":
            return Response({"error": "Leave is already in the cancelled state"}, 400)           

        noOfPaidLeaves_taken = tblleaveapply_obj.noOfPaidLeaves_taken

        if noOfPaidLeaves_taken != 0.0:
            employee_tblpaidleaves_obj = tblpaidleaves.objects.get(empID__id = int(empID))
            employee_tblpaidleaves_obj.no_of_leaves += noOfPaidLeaves_taken
            employee_tblpaidleaves_obj.save()

        tblleaveapply_obj.current_status = "Cancelled"
        tblleaveapply_obj.save()

        return Response({"detail": "Leave cancelled successfully"}, status=status.HTTP_201_CREATED)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.paid_leaves import tblpaidleavesSerializer
# from api.models import tblpaidleaves  # Ensure you import your model

class GetEmployeePaidLeaves(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all records from the tblpaidleaves table
        employees_paidleaves = tblpaidleaves.objects.all()
        
        # Serialize the queryset (note the many=True argument)
        serializer = tblpaidleavesSerializer(employees_paidleaves, many=True)
        
        # Get the serialized data
        data = serializer.data
        
        # Return the response with the serialized data
        return Response(data, status=200)
