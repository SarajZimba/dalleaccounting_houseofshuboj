# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from employee.models import Employee
# from api.serializers.employee import EmployeeSerializer

# class EmployeeGetAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             employees = Employee.objects.all()

#             serializer = EmployeeSerializer(employees, many=True)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# class EmployeeCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# class EmployeeDetailAPIView(APIView):
    
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return Response({"detail":"Employee not found"}, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk, *args, **kwargs):
#         # Get the employee object by the provided ID (primary key)
#         employee = self.get_object(pk)
        
#         # Pass the updated data to the serializer, including the existing instance
#         serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
#         # Check if the data is valid
#         if serializer.is_valid():
#             serializer.save()  # Save the changes to the instance
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, *args, **kwargs):
#         # Get the employee object by the provided ID (primary key)
#         employee = self.get_object(pk)
        
#         # Delete the employee instance
#         employee.delete()
#         return Response({"detail": "employee deleted successfully"},status=status.HTTP_200_OK)
        
        
# from api.serializers.employee import DailyAttendanceSerializer

# # class DailyAttendanceCreateAPIView(APIView):
# #     def post(self, request, *args, **kwargs):
# #         # Create a serializer instance with the incoming data
# #         serializer = DailyAttendanceSerializer(data=request.data)
        
# #         # Check if the data is valid
# #         if serializer.is_valid():
# #             # Save the new DailyAttendance record
# #             serializer.save()
# #             # Return the serialized data with a 201 Created status
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# #         # If data is invalid, return the errors with a 400 Bad Request status
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # from datetime import datetime

# # class DailyAttendanceCreateAPIView(APIView):
# #     def post(self, request, *args, **kwargs):

# #         data = request.data


# #         today_date = datetime.today().date()

# #         # Get the current time for check-in
# #         current_time = datetime.now().time()

# #         empID = data.get('empID', None)
# #         # time = data.get('time', None)

# #         if empID == None:
# #             return Response({"detail": "Please provide a employee Id"}, 400)
        
# #         employee = Employee.objects.get(id=int(empID))

# #         # check for check-in 

# #         if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
# #             employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
            
# #             # Check if the employee has already checked out
# #             # if employees_dailyattendance.check_out is not None:
# #             #     return Response({"detail": "Employee has already checked out."}, 400)
# #             employees_dailyattendance.check_out = current_time
# #             employees_dailyattendance.save()

# #             return Response({"detail": "Check out time recorded successfully"}, 200)

# #         else:
# #             create_data = {
# #                           "attendance_date":today_date,
# #                           "check_in":current_time,
# #                           "empID":int(empID)}
# #             # Create a serializer instance with the incoming data
# #             serializer = DailyAttendanceSerializer(data=create_data)

# #             # Check if the data is valid
# #             if serializer.is_valid():
# #                 # Save the new DailyAttendance record
# #                 serializer.save()
# #                 # Return the serialized data with a 201 Created status
# #                 return Response(serializer.data, status=status.HTTP_201_CREATED)
            
# #             # If data is invalid, return the errors with a 400 Bad Request status
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from api.serializers.employee import DailyAttendanceSerializer

# from datetime import datetime

# class DailyAttendanceCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):

#         data = request.data


#         today_date = datetime.today().date()

#         # Get the current time for check-in
#         current_time = datetime.now().time()

#         empID = data.get('empID', None)
#         # time = data.get('time', None)

#         if empID == None:
#             return Response({"detail": "Please provide a employee Id"}, 400)
        
#         employee = Employee.objects.get(id=int(empID))

#         # check for check-in 

#         if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#             employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)

#             # Check if the employee has already checked out
#             # if employees_dailyattendance.check_out is not None:
#             #     return Response({"detail": "Employee has already checked out."}, 400)
#             employees_dailyattendance.check_out = current_time
#             # Calculate the total time worked
#             if employees_dailyattendance.check_in is not None:
#                 check_in_time = datetime.combine(employees_dailyattendance.attendance_date, employees_dailyattendance.check_in)
#                 check_out_time = datetime.combine(employees_dailyattendance.attendance_date, current_time)
#                 total_time = check_out_time - check_in_time
#                 employees_dailyattendance.total_time = (datetime.min + total_time).time()  # Convert timedelta to time

#             employees_dailyattendance.save()

#             return Response({"detail": "Check out time recorded successfully"}, 200)

#         if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#             employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
#             employees_dailyattendance.check_out = current_time
#             employees_dailyattendance.save()

#             return Response({"detail": "Check out time recorded successfully"}, 200)

#         else:
#             create_data = {
#                           "attendance_date":today_date,
#                           "check_in":current_time,
#                           "empID":int(empID)}
#             # Create a serializer instance with the incoming data
#             serializer = DailyAttendanceSerializer(data=create_data)

#             # Check if the data is valid
#             if serializer.is_valid():
#                 # Save the new DailyAttendance record
#                 serializer.save()
#                 # Return the serialized data with a 201 Created status
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
            
#             # If data is invalid, return the errors with a 400 Bad Request status
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# from employee.models import DailyAttendance


# class DailyAttendanceDetailAPIView(APIView):
    
#     # Helper method to get the DailyAttendance object
#     def get_object(self, pk):
#         try:
#             return DailyAttendance.objects.get(pk=pk)
#         except DailyAttendance.DoesNotExist:
#             return Response({"detail":"Daily Attendance not found"}, status=status.HTTP_400_BAD_REQUEST)

#     # PATCH method to partially update a DailyAttendance record
#     def patch(self, request, pk, *args, **kwargs):
#         # Retrieve the DailyAttendance record
#         attendance = self.get_object(pk)
        
#         # Create the serializer with the existing attendance and the updated data
#         serializer = DailyAttendanceSerializer(attendance, data=request.data, partial=True)
        
#         # Check if the data is valid
#         if serializer.is_valid():
#             serializer.save()  # Save the updated data
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         # If data is invalid, return validation errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE method to delete a DailyAttendance record
#     def delete(self, request, pk, *args, **kwargs):
#         # Retrieve the DailyAttendance record
#         attendance = self.get_object(pk)
        
#         # Delete the record
#         attendance.delete()
#         return Response({"detail": "Attendance deleted successfully"}, status=status.HTTP_200_OK)
        
# class EmployeesDailyAttendanceGetAPIView(APIView):
#     """
#     API view to retrieve daily attendance for a specific employee.
#     """

#     def post(self, request, *args, **kwargs):
#         try:
#             # Validate input data
#             data = request.data
#             employee_id = data.get('employee')

#             if not employee_id:
#                 return Response({"detail": "Please provide an employee ID."}, status=status.HTTP_400_BAD_REQUEST)

#             # Fetch attendance records
#             employees_attendance = DailyAttendance.objects.filter(empID__id=int(employee_id))
            
#             if not employees_attendance.exists():
#                 return Response({"detail": "No attendance records found for the given employee."}, status=status.HTTP_404_NOT_FOUND)

#             # Serialize and return data
#             serializer = DailyAttendanceSerializer(employees_attendance, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except ValueError:
#             return Response({"detail": "Invalid employee ID provided."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
# from api.serializers.employee import PayPackageSerializer
# class PayPackageCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PayPackageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# class SearchEmployeeAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = request.data

#             employee_id = data['emp_id']
#             employees = Employee.objects.get(id=int(employee_id))

#             serializer = EmployeeSerializer(employees)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
# class GetCheckinOutStatus(APIView):
#     def get(self, request, *args, **kwargs):

#         today_date = datetime.today().date()

#         employees = Employee.objects.filter(current_status="Enrolled", attendance_required=True)

#         if employees:
#             employees_list = []
#             for employee in employees:

#                 if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#                     dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
#                     response_data = {
#                         "check-in": True,
#                         "check-in-time": dailyattendance.check_in,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name,
#                         "total_time": dailyattendance.total_time,
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,
#                     }

#                     if dailyattendance.check_out is not None:
#                         response_data["check-out"] = True
#                         response_data["check-out-time"] = dailyattendance.check_out
#                 else:
#                     response_data = {
#                         "check-in": False,
#                         "check-in-time": None,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name, 
#                         "total_time": None,
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,
#                     }
#                 employees_list.append(response_data)
#             return Response(employees_list, 200)
#         else:
#             return Response("no active employees found", 400)
            
# class GetAllDailyAttendance(APIView):
#     def get(self, request, *args, **kwargs):

#         today_date = datetime.today().date()

#         employees = Employee.objects.all()

#         if employees:
#             employees_list = []
#             for employee in employees:

#                 if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#                     dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
#                     response_data = {
#                         "check-in": True,
#                         "check-in-time": dailyattendance.check_in,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name,
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,
#                     }

#                     if dailyattendance.check_out is not None:
#                         response_data["check-out"] = True
#                         response_data["check-out-time"] = dailyattendance.check_out
#                 else:
#                     response_data = {
#                         "check-in": False,
#                         "check-in-time": None,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name,    
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,             
#                     }
#                 employees_list.append(response_data)
#             return Response(employees_list, 200)
#         else:
#             return Response("no active employees found", 400)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from employee.models import Employee
from api.serializers.employee import EmployeeSerializer
from employee.models import tblpaidleaves
from organization.models import Organization


# class EmployeeGetAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             employees = Employee.objects.all()

#             serializer = EmployeeSerializer(employees, many=True)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class EmployeeGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            today_date = datetime.today().date()
            employees = Employee.objects.filter(current_status="Enrolled")

            serializer = EmployeeSerializer(employees, many=True)

            employees_count = Employee.objects.filter(current_status="Enrolled").count()

            enrolled_employees = Employee.objects.all()
            married_employees_count = enrolled_employees.filter(marital_status="Married").count()
            unmarried_employees_count = enrolled_employees.filter(marital_status="Unmarried").count()
            divorced_employees_count = enrolled_employees.filter(marital_status="Divorced").count()
            male_employees_count = enrolled_employees.filter(gender="male").count()
            female_employees_count = enrolled_employees.filter(gender="female").count()
            # Check if the employee is on leave today
            # count_employees_on_leave = tblleaveapply.objects.filter(
            #         leaveDateFrom__lte=today_date,
            #         leaveDateTo__gte=today_date,
            #         current_status = "Approved"
            #     ).count()
            # no_of_approved_leaves = tblleaveapply.objects.filter(
            #         current_status = "Approved"
            #     ).count()
            # no_of_pending_leaves = tblleaveapply.objects.filter(
            #         current_status = None
            #     ).count()
            
            
            response_data = {
                "employees" : serializer.data,
                "employees_count" : employees_count,
                "married" :married_employees_count,
                "unmarried" :unmarried_employees_count,
                "divorced" :divorced_employees_count,
                "male" :male_employees_count,
                "female" :female_employees_count
                # "on_leave" :count_employees_on_leave,
                # "approved_leaves" :no_of_approved_leaves,
                # "pending_leaves" :no_of_pending_leaves,
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            
            
class AllEmployeeGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            today_date = datetime.today().date()
            employees = Employee.objects.all()

            serializer = EmployeeSerializer(employees, many=True)

            employees_count = Employee.objects.all().count()

            enrolled_employees = Employee.objects.all()
            married_employees_count = enrolled_employees.filter(marital_status="Married").count()
            unmarried_employees_count = enrolled_employees.filter(marital_status="Unmarried").count()
            divorced_employees_count = enrolled_employees.filter(marital_status="Divorced").count()
            male_employees_count = enrolled_employees.filter(gender="male").count()
            female_employees_count = enrolled_employees.filter(gender="female").count()
            # Check if the employee is on leave today
                                                                                                 
            
            
            response_data = {
                "employees" : serializer.data,
                "employees_count" : employees_count,
                "married" :married_employees_count,
                "unmarried" :unmarried_employees_count,
                "divorced" :divorced_employees_count,
                "male" :male_employees_count,
                "female" :female_employees_count
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            
            
from api.serializers.employee import EmployeePayPackageSerializer

class EmployeeCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        org_paidleaves = Organization.objects.first().noOfpaidleavesallowed
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee_instance = serializer.save()
            tblpaidleaves.objects.create(empID=employee_instance, no_of_leaves = org_paidleaves)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SearchEmployeeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            employee_id = data['emp_id']
            employees = Employee.objects.get(id=int(employee_id))

            serializer = EmployeePayPackageSerializer(employees)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
class GetCheckinOutStatus(APIView):
    def get(self, request, *args, **kwargs):

        today_date = datetime.today().date()

        employees = Employee.objects.filter(current_status="Enrolled", attendance_required=True)

        if employees:
            employees_list = []
            for employee in employees:

                if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
                    dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee, empID__attendance_required=True)
                    response_data = {
                        "check-in": True,
                        "check-in-time": dailyattendance.check_in,
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": employee.lateattendance_alert,
                    }

                    if dailyattendance.check_out is not None:
                        response_data["check-out"] = True
                        response_data["check-out-time"] = dailyattendance.check_out
                else:
                    response_data = {
                        "check-in": False,
                        "check-in-time": None,
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,    
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": employee.lateattendance_alert,             
                    }
                employees_list.append(response_data)
            return Response(employees_list, 200)
        else:
            return Response("no active employees found", 400)


                
class EmployeeDetailAPIView(APIView):
    
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Response({"detail":"Employee not found"}, code=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        # Get the employee object by the provided ID (primary key)
        employee = self.get_object(pk)
        
        # Pass the updated data to the serializer, including the existing instance which will only update the fields sent in the body
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
        # Check if the data is valid
        if serializer.is_valid():
            serializer.save()  # Save the changes to the instance
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        # Get the employee object by the provided ID (primary key)
        employee = self.get_object(pk)
        
        # Delete the employee instance
        employee.delete()
        return Response({"detail": "employee deleted successfully"},status=status.HTTP_200_OK)
    

from api.serializers.employee import DailyAttendanceSerializer

from datetime import datetime, timedelta
from organization.models import Organization

class DailyAttendanceCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data

        org = Organization.objects.first()

        arrival_time = org.arrival_time

        today_date = datetime.today().date()

        # Get the current time for check-in
        current_time = datetime.now().time()

        empID = data.get('empID', None)
        # time = data.get('time', None)

        if empID == None:
            return Response({"detail": "Please provide a employee Id"}, 400)
        
        employee = Employee.objects.get(id=int(empID))
        
        # Convert arrival_time and current_time to datetime for comparison
        today_datetime = datetime.combine(today_date, arrival_time)
        current_datetime = datetime.combine(today_date, current_time)

        late_attendance_flag = False
        no_show_flag = False


        # # Check if current time is more than 30 minutes after arrival time
        # if current_datetime > today_datetime + timedelta(minutes=30):
        #     no_show_flag = True
        if current_datetime > today_datetime:
            if current_datetime <= today_datetime + timedelta(minutes=15):
                print(current_datetime)
                print(today_datetime)
                late_attendance_flag = False
                no_show_flag = False
            else:
                late_attendance_flag = True
                no_show_flag = False
            # Check if current time is within 15 minutes of arrival time

        # else:

        #     late_attendance_flag = False
        #     no_show_flag = False

        # check for check-in 

        if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
            employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)

            # Check if the employee has already checked out
            # if employees_dailyattendance.check_out is not None:
            #     return Response({"detail": "Employee has already checked out."}, 400)
            employees_dailyattendance.check_out = current_time
            # Calculate the total time worked
            if employees_dailyattendance.check_in is not None:
                check_in_time = datetime.combine(employees_dailyattendance.attendance_date, employees_dailyattendance.check_in)
                check_out_time = datetime.combine(employees_dailyattendance.attendance_date, current_time)
                total_time = check_out_time - check_in_time
                employees_dailyattendance.total_time = (datetime.min + total_time).time()  # Convert timedelta to time

            employees_dailyattendance.save()

            return Response({"detail": "Check out time recorded successfully"}, 200)

        # if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
        #     employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
        #     employees_dailyattendance.check_out = current_time
        #     employees_dailyattendance.save()

        #     return Response({"detail": "Check out time recorded successfully"}, 200)

        else:
            create_data = {
                           "attendance_date":today_date,
                           "check_in":current_time,
                           "empID":int(empID),
                            "late_attendance_flag" : late_attendance_flag,
                            "no_show_flag": no_show_flag}
            # Create a serializer instance with the incoming data
            serializer = DailyAttendanceSerializer(data=create_data)

            # Check if the data is valid
            if serializer.is_valid():
                # Save the new DailyAttendance record
                serializer.save()
                # Return the serialized data with a 201 Created status
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # If data is invalid, return the errors with a 400 Bad Request status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from employee.models import DailyAttendance


class DailyAttendanceDetailAPIView(APIView):
    
    # Helper method to get the DailyAttendance object
    def get_object(self, pk):
        try:
            return DailyAttendance.objects.get(pk=pk)
        except DailyAttendance.DoesNotExist:
            return Response({"detail":"Daily Attendance not found"}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a DailyAttendance record
    def patch(self, request, pk, *args, **kwargs):
        # Retrieve the DailyAttendance record
        attendance = self.get_object(pk)
        
        # Create the serializer with the existing attendance and the updated data with partial=True which will only update the fields sent
        serializer = DailyAttendanceSerializer(attendance, data=request.data, partial=True)
        
        # Check if the data is valid
        if serializer.is_valid():
            serializer.save()  # Save the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If data is invalid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a DailyAttendance record
    def delete(self, request, pk, *args, **kwargs):
        # Retrieve the DailyAttendance record
        attendance = self.get_object(pk)
        
        # Delete the record
        attendance.delete()
        return Response({"detail": "Attendance deleted successfully"}, status=status.HTTP_200_OK)

class EmployeesDailyAttendanceGetAPIView(APIView):
    """
    API view to retrieve daily attendance for a specific employee.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Validate input data
            data = request.data
            employee_id = data.get('employee')

            if not employee_id:
                return Response({"detail": "Please provide an employee ID."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch attendance records
            employees_attendance = DailyAttendance.objects.filter(empID__id=int(employee_id))
            
            if not employees_attendance.exists():
                return Response({"detail": "No attendance records found for the given employee."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize and return data
            serializer = DailyAttendanceSerializer(employees_attendance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"detail": "Invalid employee ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# from api.serializers.employee import PayPackageSerializer
# class PayPackageCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PayPackageSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from api.serializers.employee import PayPackageSerializer
from decimal import Decimal
from employee.models import tblEmployeeSalary
class PayPackageCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = request.data
        serializer = PayPackageSerializer(data=posted_data, many=True)


        if serializer.is_valid():
            serializer.save()

            total = Decimal(0.0)
            taxable = Decimal(0.0)
            non_taxable = Decimal(0.0)
            for data in posted_data:
                total += Decimal(data["amount"])
                if data["taxable"]:
                    taxable += Decimal(data["amount"])
                else:
                    non_taxable += Decimal(data["amount"])

            empID = posted_data[0]["empID"]

            employee = Employee.objects.get(id=int(empID))

            if tblEmployeeSalary.objects.filter(emp_ID=employee).exists():
                employee_salaryobj = tblEmployeeSalary.objects.get(emp_ID=employee)
                employee_salaryobj.total_salary += total
                employee_salaryobj.taxable += taxable
                employee_salaryobj.non_taxable += non_taxable
                employee_salaryobj.save()
            else:
                tblEmployeeSalary.objects.create(emp_ID=employee, total_salary=total, taxable=taxable, non_taxable=non_taxable)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from employee.models import tblleaveapply
class GetAllDailyAttendance(APIView):
    def get(self, request, *args, **kwargs):

        today_date = datetime.today().date()

        employees = Employee.objects.filter(current_status="Enrolled", attendance_required=True)

        count_employees_on_leave = tblleaveapply.objects.filter(
                    empID__current_status = "Enrolled",
                    leaveDateFrom__lte=today_date,
                    leaveDateTo__gte=today_date,
                    current_status = "Approved"
                ).count()
        no_of_approved_leaves = tblleaveapply.objects.filter(
                    current_status = "Approved",empID__current_status = "Enrolled"
                ).count()
        no_of_pending_leaves = tblleaveapply.objects.filter(
                    current_status = None,empID__current_status = "Enrolled"
                ).count()
        # late_attendance_flag = models.BooleanField(null=True)
        # no_show_flag = models.BooleanField(null=True)
        no_of_late_arrival = DailyAttendance.objects.filter(late_attendance_flag=True, attendance_date=today_date, empID__current_status="Enrolled", empID__attendance_required=True).count()
        # no_show= DailyAttendance.objects.filter(no_show_flag=True, attendance_date=today_date, empID__current_status="Enrolled", empID__attendance_required=True).count()

        if employees:
            employees_list = []
            for employee in employees:
                # Check if the employee is on leave today
                on_leave = tblleaveapply.objects.filter(
                    empID=employee,
                    leaveDateFrom__lte=today_date,
                    leaveDateTo__gte=today_date,
                    current_status = "Approved"
                ).exists()
                if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
                    dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
                    response_data = {
                        "check-in": True,
                        "check-in-time": dailyattendance.check_in.strftime('%I:%M %p'),
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": dailyattendance.late_attendance_flag,
                        "no_show": dailyattendance.no_show_flag,
                        "type": employee.type,
                        "leave": on_leave  # Add leave status to response

                    }

                    if dailyattendance.check_out is not None:
                        response_data["check-out"] = True
                        response_data["check-out-time"] = dailyattendance.check_out.strftime('%I:%M %p')
                else:
                    # dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)

                    if on_leave:
                        no_show = False
                    else:
                        org = Organization.objects.last()
                        arrival_time = org.arrival_time
                        today_date = datetime.today().date()
                        
                        # Get the current time for check-in
                        current_time = datetime.now().time()
                        
                        # Convert arrival_time and current_time to datetime for comparison
                        today_datetime = datetime.combine(today_date, arrival_time)
                        current_datetime = datetime.combine(today_date, current_time)
                        no_show = True


                        # # Check if current time is more than 30 minutes after arrival time
                        # if current_datetime > today_datetime + timedelta(minutes=30):
                        #     no_show_flag = True
                        if current_datetime > today_datetime:
                            if current_datetime <= today_datetime + timedelta(minutes=30):
                                no_show= False
                            else:
                                no_show=True
                        else:
                            no_show=False

                    response_data = {
                        "check-in": False,
                        "check-in-time": None,
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,    
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": False,
                        "no_show": no_show,
                        "type": employee.type,
                        "leave": on_leave  # Add leave status to response

                    }
                employees_list.append(response_data)
            no_of_employees = employees.count()
            no_show= DailyAttendance.objects.filter(attendance_date=today_date,empID__current_status="Enrolled", no_show_flag=False, empID__attendance_required=True).count()
            no_of_on_leave = tblleaveapply.objects.filter(
                        leaveDateFrom__lte=today_date,
                        leaveDateTo__gte=today_date,
                        current_status = "Approved",
                        empID__current_status="Enrolled",
                        empID__attendance_required=True
                    ).count()
    
            no_of_no_show = sum(employee["no_show"] for employee in employees_list) 
            response_data = {
                "employee_list" : employees_list,
                "on_leave" :count_employees_on_leave,
                "approved_leaves" :no_of_approved_leaves,
                "pending_leaves" :no_of_pending_leaves,
                "no_of_late_arrival" : no_of_late_arrival,
                "no_show": no_of_no_show,
                "arrival_time" : Organization.objects.first().arrival_time,
                "clock_out_time" : Organization.objects.first().clock_out_time
            }
            return Response(response_data, 200)
        else:
            return Response("no active employees found", 400)
    
from employee.models import Pay_Package
class RemovePayPackage(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        package_id = data.get('package_id', None)

        if package_id is None:
            return Response({"error": "The package id cannot be Null"}, 400)
        try:
            package = Pay_Package.objects.get(id=int(package_id))
        except Exception as e:
            return Response({"error": "No package found of that passed Id"}, 400)

        package.delete()

        return Response({"detail":"Package has been removed successfully"}, 200)

from api.serializers.employee import MasterPayPackageSerializer
from decimal import Decimal
from employee.models import MasterPayPackage
class MasterPayPackageListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            all_packages = MasterPayPackage.objects.all()

            serializer = MasterPayPackageSerializer(all_packages, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        posted_data = request.data
        serializer = MasterPayPackageSerializer(data=posted_data, many=True)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Data is not valid"}, 400)

class CheckinTime(APIView):
    def get(self, request, *args, **kwargs):
        org = Organization.objects.first()

        if org is None:
            return Response({"No organization found", 400})
        arrival_time = org.arrival_time

        return Response({"arrival_time": arrival_time}, 200)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models import tblEmployeeCIT
from api.serializers.employee import tblEmployeeCITSerializer

class EmployeeCITAPI(APIView):
    def get(self, request):
        """Fetch all Employee CIT records."""
        employees = tblEmployeeCIT.objects.all()
        serializer = tblEmployeeCITSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create multiple Employee CIT records."""
        if isinstance(request.data, list):  # If multiple objects are posted
            serializer = tblEmployeeCITSerializer(data=request.data, many=True)
        else:  # If a single object is posted
            serializer = tblEmployeeCITSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models import tblEmployeeCIT
from api.serializers.employee import tblEmployeeCITSerializer

class UpdateEmployeeCITAPI(APIView):
    def put(self, request, pk):
        """Update an Employee CIT record."""
        try:
            employee_cit = tblEmployeeCIT.objects.get(id=pk)
        except tblEmployeeCIT.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = tblEmployeeCITSerializer(employee_cit, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteEmployeeCITAPI(APIView):
    def delete(self, request, pk):
        """Delete an Employee CIT record."""
        try:
            employee_cit = tblEmployeeCIT.objects.get(id=pk)
        except tblEmployeeCIT.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        employee_cit.delete()
        return Response({"detail": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
