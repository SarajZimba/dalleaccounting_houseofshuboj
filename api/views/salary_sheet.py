from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from employee.models import Employee, Pay_Package, tblleaveapply,MasterPayPackage, tblpaidleaves
from api.serializers.employee import PayPackageSerializer
from django.db.models import Sum
from datetime import datetime
from employee.models import tblDeduction
from salary.utils import calculate_net_salary, calculate_tax, calculate_totals, get_nepali_date
import nepali_datetime
from organization.models import Organization
from employee.models import tblEmployeeCommision

class SalarySlip(APIView):
    

    def post(self, request, *args, **kwargs):
        data = request.data
        employee = data["empID"]
        current_date = datetime.today()

        # Get the current month and year
        current_year = current_date.year
        current_month = current_date.month
        try:
            employee_obj = Employee.objects.get(id=int(employee))

        except Exception as e:
            return Response({"error": "Employee does not exists"}, 400)
        # total_gross_salary part
        pay_packages = Pay_Package.objects.filter(empID = employee_obj)

        packagetotal_sum = pay_packages.aggregate(Sum('amount'))['amount__sum']

        total_amount = packagetotal_sum if packagetotal_sum is not None else 0  # If None, set it to 0

        # payPackageSeriailized_data = PayPackageSerializer(pay_packages, many=True)
        employee_package_dict = {}
        for pay_package in pay_packages:
            package_name = pay_package.package.package_name if pay_package.package else None
            amount = pay_package.package.amount if pay_package.package else None
            package_type = pay_package.package.package_type if pay_package.package else None
            taxable = pay_package.package.taxable if pay_package.package else None

            employee_package_data = {
                "package_name" : package_name,
                "amount" : amount,
                "package_type" : package_type,
                "taxable" : taxable
            }
            # Add the package to the dictionary with the package_name as the key
            if package_name:  # Ensure the package_name is not None
                employee_package_dict[package_name] = employee_package_data

            # Fetch all MasterPayPackage entries
        all_master_pay_packages = MasterPayPackage.objects.all()

        # Iterate over each MasterPayPackage and check if it's in the employee_package_dict
        for master_package in all_master_pay_packages:
            package_name = master_package.package_name

            # If the package is not in the employee_package_dict, add it with dummy data
            if package_name not in employee_package_dict:
                dummy_data = {
                    "package_name": package_name,
                    "amount": 0,  # Set amount to 0 for missing packages
                    "package_type": master_package.package_type,
                    "taxable": master_package.taxable
                }
                employee_package_dict[package_name] = dummy_data
            
            # Now extract the values of the dictionary into a list
        employee_package_list = list(employee_package_dict.values())


        # response_data = {"name": "", "total_gross_salary": {}, "total_deductions": {}}
        response_data = {"name": "", "total_gross_salary": {}}

        response_data["name"] = employee_obj.name
        response_data["empID"] = employee_obj.id
        response_data["total_gross_salary"]["paypackages"] = employee_package_list
        response_data["total_gross_salary"]["total_salary"] = total_amount
        

        # # total_deductions_part

        # leaves = tblleaveapply.objects.filter(current_status="Approved", empID=employee_obj,applyDate__year=current_year,applyDate__month=current_month)

        # # Sum of noOfDays where noOfUnPaidLeaves = 0.0 (paid leaves)
        # paid_leaves_sum = leaves.filter(noOfUnPaidLeaves=0.0).aggregate(Sum('noOfDays'))['noOfDays__sum']

        # # Sum of noOfDays where noOfPaidLeaves = 0.0 (unpaid leaves)
        # unpaid_leaves_sum = leaves.filter(noOfPaidLeaves=0.0).aggregate(Sum('noOfDays'))['noOfDays__sum']

        # # If no matching records, the aggregate will return None, so you should set it to 0
        # paid_leaves_sum = paid_leaves_sum if paid_leaves_sum is not None else 0
        # unpaid_leaves_sum = unpaid_leaves_sum if unpaid_leaves_sum is not None else 0

        # unpaid_leavesdeduction = round(float(unpaid_leaves_sum) * float(total_amount/20), 2)

        # response_data["total_deductions"]["paid_leaves"] = paid_leaves_sum
        # response_data["total_deductions"]["unpaid_leavesdeduction"] = unpaid_leavesdeduction
        # response_data["total_deductions"]["unpaid_leaves"] = unpaid_leaves_sum
        



        return Response(response_data, 200)

from decimal import Decimal

import nepali_datetime
from django.db.models import Q
from decimal import Decimal
from datetime import date
import json

class SalarySheet(APIView):
    def get(self, request, *args, **kwargs):
        # current_date = datetime.today()

        # # Get the current month and year
        # current_year = current_date.year
        # current_month = current_date.month
        
        current_date = date.today()

        # Convert current date to Nepali date
        nepali_today = nepali_datetime.date.from_datetime_date(current_date)
        current_nepali_year = nepali_today.year
        dashain_month = Organization.objects.last().dashain_month
        current_nepali_month = nepali_today.strftime("%B")  # Get the Nepali month name

        try:
            employees = Employee.objects.filter(current_status="Enrolled")

        except Exception as e:
            return Response({"error": "Employees does not exists"}, 400)
        # total_gross_salary part
        response_list = []
        for employee_obj in employees:
            pay_packages = Pay_Package.objects.filter(empID = employee_obj)

            packagetotal_sum = pay_packages.aggregate(Sum('amount'))['amount__sum']

            total_amount = packagetotal_sum if packagetotal_sum is not None else 0  # If None, set it to 0

            # payPackageSeriailized_data = PayPackageSerializer(pay_packages, many=True)
            employee_package_dict = {}
            for pay_package in pay_packages:
                package_name = pay_package.package.package_name if pay_package.package else None
                # amount = pay_package.package.amount if pay_package.package else None
                amount = pay_package.amount if pay_package.amount else 0.0
                package_type = pay_package.package.package_type if pay_package.package else None
                taxable = pay_package.package.taxable if pay_package.package else None

                employee_package_data = {
                    "package_name" : package_name,
                    "amount" : amount,
                    "package_type" : package_type,
                    "taxable" : taxable
                }
                # Add the package to the dictionary with the package_name as the key
                if package_name:  # Ensure the package_name is not None
                    employee_package_dict[package_name] = employee_package_data

            # Fetch all MasterPayPackage entries
            all_master_pay_packages = MasterPayPackage.objects.all()

            # Iterate over each MasterPayPackage and check if it's in the employee_package_dict
            for master_package in all_master_pay_packages:
                package_name = master_package.package_name

                # If the package is not in the employee_package_dict, add it with dummy data
                if package_name not in employee_package_dict:
                    dummy_data = {
                        "package_name": package_name,
                        "amount": 0.0,  # Set amount to 0 for missing packages
                        "package_type": master_package.package_type,
                        "taxable": master_package.taxable
                    }
                    employee_package_dict[package_name] = dummy_data

            if current_nepali_month == dashain_month:
                package_name = "Dashain Bonus"
                dashain_package = {
                        "package_name": package_name,
                        "amount": pay_packages.filter(package__package_name="Basic Salary").first().amount,  # Set amount to 0 for missing packages
                        "package_type": "Bonus",
                        "taxable": False
                    }
                employee_package_dict[package_name] = dashain_package
                
            commisions = tblEmployeeCommision.objects.filter(empID=employee_obj, month=current_nepali_month)

            for commision in commisions:
                # package_name = "Commision Bonus"
                print(commision)
                commision_package = {
                            "package_name": commision.type,
                            "amount": commision.amount,  # Set amount to 0 for missing packages
                            "package_type": "Bonus",
                            "taxable": False
                    }
                employee_package_dict[commision.type] = commision_package
            # # Now extract the values of the dictionary into a list
            # employee_package_list = list(employee_package_dict.values())
            # Extract the values of the dictionary into a list and sort by package_name
            employee_package_list = sorted(
                employee_package_dict.values(),
                key=lambda x: x['package_name']
            )

            # response_data = {"name": "", "total_gross_salary": {}, "total_deductions": {}}
            # response_data = {"name": "", "total_gross_salary": {}}
            response_data = {"name": "", "total_gross_salary": {}, "leave_deductions": {}}


            response_data["name"] = employee_obj.name
            response_data["empID"] = employee_obj.id

            response_data["total_gross_salary"]["paypackages"] = employee_package_list
            
            # total_leavesdeductions_part

            # leaves = tblleaveapply.objects.filter(current_status="Approved", empID=employee_obj,applyDate__year=current_year,applyDate__month=current_month)

            leaves = tblleaveapply.objects.filter(
                Q(nepali_year=current_nepali_year) &  # Match Nepali year
                Q(nepali_month__icontains=f'"{current_nepali_month}"') &  # Check if current month exists in JSON
                Q(current_status="Approved") & 
                Q(empID=employee_obj)
            )
            # Initialize variables for paid and unpaid leave days
            paid_leaves_sum = 0
            unpaid_leaves_sum = 0

            # Iterate through the filtered leaves
            for leave in leaves:
                # Parse the Nepali month JSON field into a Python dictionary
                nepali_month_data = json.loads(leave.nepali_month)
                print(nepali_month_data)
                # Get the leave days for the current month
                current_month_leave_days = nepali_month_data.get(current_nepali_month, 0)

                # Calculate paid and unpaid leave days based on the `noOfUnPaidLeaves` and `noOfPaidLeaves` fields
                if leave.noOfUnPaidLeaves == 0.0:
                    paid_leaves_sum += current_month_leave_days
                if leave.noOfPaidLeaves == 0.0:
                    unpaid_leaves_sum += current_month_leave_days

            # If no matching records, the aggregate will return None, so you should set it to 0
            paid_leaves_sum = paid_leaves_sum if paid_leaves_sum is not None else 0
            unpaid_leaves_sum = unpaid_leaves_sum if unpaid_leaves_sum is not None else 0

            unpaid_leavesdeduction = round(float(unpaid_leaves_sum) * float(total_amount/20), 2)

            # response_data["leave_deductions"]["paid_leaves"] = paid_leaves_sum
            response_data["leave_deductions"]["unpaid_leavesdeduction"] = unpaid_leavesdeduction
            response_data["leave_deductions"]["unpaid_leaves"] = unpaid_leaves_sum
            # response_data["net_payable"] = round(float(total_amount) - float(unpaid_leavesdeduction), 2)

            total_amount -= Decimal(unpaid_leavesdeduction)
            response_data["total_gross_salary"]["total_salary"] = total_amount  
            
            deductions = tblDeduction.objects.filter(used=True)

            deduction_list = []
            # deduction_data = {}
            if deductions:
                for deduction in deductions:


                    deduction_data = {
                            "name": deduction.name,
                            "amount": 0.0
                    }
                    if deduction.name == "Social Security Fund":
                        # if total_amount <= 500000:
                        #     deduction_data["amount"] = round(float(total_amount)*0.01, 2)
                        basic_salary_package =  pay_packages.filter(package__package_name="Basic Salary").first()
                        if basic_salary_package:
                            basic_salary_amount = basic_salary_package.amount
                            if unpaid_leaves_sum != 0.0:
                                basic_salary_amount = basic_salary_amount - (basic_salary_amount/20) * unpaid_leaves_sum 
                        else:
                            basic_salary_amount = Decimal(0.0)
                        ssf_amount = basic_salary_amount * Decimal(0.11)
                        deduction_data["amount"] = ssf_amount
                        total_amount -= ssf_amount
                        deduction_tax = calculate_tax(total_amount,"sst_deduct_false")
                    if deduction.name == "Employees Provident Fund":
                        epf_amount = round(Decimal(total_amount) * Decimal(0.1), 2)
                        deduction_data["amount"] = epf_amount
                        total_amount -= epf_amount
                        deduction_tax = calculate_tax(total_amount, "sst_deduct_true")
                    deduction_list.append(deduction_data)
            else:
                deduction_tax = calculate_tax(total_amount, "sst_deduct_true")

            net_salary = calculate_net_salary(total_amount, deduction_tax)

            response_data["net_amount"] = net_salary
            response_data["fund_deductions"] = deduction_list


            response_data["tax_deduction"] = deduction_tax
            response_list.append(response_data)
            
        totals = calculate_totals(response_list)
        month, nepali_date = get_nepali_date()
        fiscal_year = Organization.objects.last().current_fiscal_year
        final_response = {
            "response_list" : response_list,
            "month" : month,
            "nepali_date": nepali_date,
            "totals" : totals,
            "fiscal_year":fiscal_year
        }
        # return Response(response_list, 200)
        return Response(final_response, 200)
        
from salary.models import MonthlySalaryReport, EmployeeSalary, EmployeeSalaryPayPackage, LeaveDeduction, FundDeduction, TaxDeduction, Total


# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import MonthlySalaryReport, Total, EmployeeSalary, EmployeeSalaryPayPackage, LeaveDeduction, FundDeduction, TaxDeduction
from django.db import transaction
from salary.salaryjournal_utils import salaryjournalentry

class MonthlySalaryReportCreateView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            # Create or update MonthlySalaryReport
            month = data.get("month")
            nepali_date = data.get("nepali_date")
            totals = data.get("totals", {})
            today_nepaliYear = nepali_datetime.date.today().strftime("%Y")

            fiscal_year = Organization.objects.last().current_fiscal_year

            monthly_report = MonthlySalaryReport.objects.filter(
                    month=month,
                    nepali_date=nepali_date,
                    nepali_year= today_nepaliYear,
                    fiscal_year=fiscal_year
            )

            if monthly_report:
                return Response(f"Salary for this {month} for {today_nepaliYear} is already upoaded")

            monthly_report= MonthlySalaryReport.objects.create(
                month=month,
                nepali_date=nepali_date,
                nepali_year= today_nepaliYear,
                fiscal_year=fiscal_year

            )

            # Saving total amounts to Total model
            for key, value in totals.items():
                if key and value is not None:
                    Total.objects.create(
                        name=key,
                        amount=value,
                        monthlysalary=monthly_report
                    )

            # Process each employee's salary details
            response_list = data.get("response_list", [])
            
            for employee_data in response_list:
                empID = employee_data.get("empID")
                employee = Employee.objects.get(id=empID)
                name = employee_data.get("name")
                net_amount = employee_data.get("net_amount")
                total_salary = employee_data.get("total_gross_salary", {}).get("total_salary", 0)

                # Create or update EmployeeSalary instance
                employee_salary, created = EmployeeSalary.objects.get_or_create(
                    empID=employee,
                    name=name,
                )
                employee_salary.total_salary = total_salary
                employee_salary.net_amount = net_amount
                employee_salary.monthly_report = monthly_report
                employee_salary.save()

                # Save Pay Packages for this employee
                paypackages = employee_data.get("total_gross_salary", {}).get("paypackages", [])
                for package in paypackages:
                    package_name = package.get("package_name")
                    amount = package.get("amount")

                    EmployeeSalaryPayPackage.objects.create(
                        employee=employee_salary,
                        package_name=package_name,
                        amount=amount
                    )

                # Save Leave Deductions for this employee
                leave_deductions = employee_data.get("leave_deductions", {})
                unpaid_leavesdeduction = leave_deductions.get("unpaid_leavesdeduction", 0)
                unpaid_leaves = leave_deductions.get("unpaid_leaves", 0)

                LeaveDeduction.objects.create(
                    employee=employee_salary,
                    unpaid_leavesdeduction=unpaid_leavesdeduction,
                    unpaid_leaves=unpaid_leaves
                )

                # Save Fund Deductions for this employee
                fund_deductions = employee_data.get("fund_deductions", [])
                for fund in fund_deductions:
                    fund_name = fund.get("name")
                    fund_amount = fund.get("amount")
                    
                    FundDeduction.objects.create(
                        employee=employee_salary,
                        name=fund_name,
                        amount=fund_amount
                    )

                # Save Tax Deductions for this employee
                tax_deductions = employee_data.get("tax_deduction", [])
                for tax in tax_deductions:
                    tax_name = tax.get("name")
                    tax_total = tax.get("Total", 0)

                    TaxDeduction.objects.create(
                        employee=employee_salary,
                        name=tax_name,
                        total=tax_total
                    )
                try:
                    paid_leaves_obj = tblpaidleaves.objects.get(empID=employee)
                    org_paidleaves = Organization.objects.first().noOfpaidleavesallowed
                    paid_leaves_obj.no_of_leaves += org_paidleaves
                    paid_leaves_obj.save()
                except Exception as e:
                    return Response({"error": "No paidleaves data found for this employee"})
            try:
                salaryjournalentry(data)
                print("salary journal called")
            except Exception as e:
                # raise e
                print(str(e))
            return Response({"message": "Salary report and employee data saved successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from datetime import datetime

class GetMonthlySalaryReportAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Get the current Nepali year (e.g., 2081)

            data = request.data

            month = data.get("month_name", None)
            current_nepali_year = self.get_current_nepali_year()

            # Filter MonthlySalaryReport by current Nepali year
            reports = MonthlySalaryReport.objects.filter(nepali_year=current_nepali_year, month=month)

            # # Prepare the response data
            # response_list = []
            for report in reports:
                # Prepare the monthly salary data for each report
                monthly_data = {
                    "month": report.month,
                    "nepali_date": report.nepali_date,
                    "totals": self.get_totals_for_report(report),
                    "response_list": self.get_employee_data_for_report(report),
                    "fiscal_year": report.fiscal_year
                }
                # response_list.append(monthly_data)

            return Response(monthly_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_current_nepali_year(self):
        # This method can either return the current Nepali year from the system, 
        # or you can calculate it based on the current date using a Nepali date conversion library
        # For simplicity, we'll return a static value as an example (e.g., 2081)
        
        # Assuming the current Nepali year is 2081, replace it with actual calculation if necessary
        nepali_year = nepali_datetime.date.today().strftime("%Y")
        return str(nepali_year)

    def get_totals_for_report(self, report):
        # Get all totals for the given MonthlySalaryReport instance
        totals_data = Total.objects.filter(monthlysalary=report)

        totals = {}
        for total in totals_data:
            print(total)
            totals[total.name] = str(total.amount)  # Convert amounts to string to match the requested response format

        return totals

    def get_employee_data_for_report(self, report):
        # Get all employees linked to this MonthlySalaryReport
        employee_salaries = EmployeeSalary.objects.filter(monthly_report=report)

        employee_data_list = []
        for employee in employee_salaries:
            # Get pay packages for the employee
            paypackages = EmployeeSalaryPayPackage.objects.filter(employee=employee)
            paypackage_list = []
            for package in paypackages:
                paypackage_list.append({
                    "package_name": package.package_name,
                    "amount": str(package.amount),
                    "package_type": "",
                    "taxable": False
                })
            paypackage_list = sorted(paypackage_list, key=lambda x: x['package_name'])
            # Get leave deductions for the employee
            leave_deductions = LeaveDeduction.objects.filter(employee=employee).first()
            leave_deduction_data = {
                "unpaid_leavesdeduction": str(leave_deductions.unpaid_leavesdeduction) if leave_deductions else "0",
                "unpaid_leaves": str(leave_deductions.unpaid_leaves) if leave_deductions else "0"
            }

            # Get fund deductions for the employee
            fund_deductions = FundDeduction.objects.filter(employee=employee)
            fund_deduction_list = []
            for fund in fund_deductions:
                fund_deduction_list.append({
                    "name": fund.name,
                    "amount": str(fund.amount)
                })

            # Get tax deductions for the employee
            tax_deductions = TaxDeduction.objects.filter(employee=employee)
            tax_deduction_list = []
            for tax in tax_deductions:
                tax_deduction_list.append({
                    "name": tax.name,
                    "Total": str(tax.total)
                })

            employee_data = {
                "name": employee.name,
                "total_gross_salary": {
                    "paypackages": paypackage_list,
                    "total_salary": str(employee.total_salary)
                },
                "leave_deductions": leave_deduction_data,
                "empID": employee.empID.id,
                "fund_deductions": fund_deduction_list,
                "tax_deduction": tax_deduction_list,
                "net_amount" : employee.net_amount
            }

            employee_data_list.append(employee_data)

        return employee_data_list

from datetime import datetime

class GetOneYearMonthWiseSalaryReportAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Get the current Nepali year (e.g., 2081)

            data = request.data

            empID = data.get("empID", None)
            employee = Employee.objects.get(id=int(empID))
            current_nepali_year = self.get_current_nepali_year()

            # Filter MonthlySalaryReport by current Nepali year
            reports = MonthlySalaryReport.objects.filter(nepali_year=current_nepali_year)

            # Prepare the response data
            response_list = []
            for report in reports:
                # Prepare the monthly salary data for each report
                monthly_data = {
                    "month": report.month,
                    "nepali_date": report.nepali_date,
                    # "totals": self.get_totals_for_report(report),
                    "fiscal_year": report.fiscal_year,
                    "response_list": self.get_employee_data_for_report(report, employee)
                }
                response_list.append(monthly_data)

            return Response(response_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_current_nepali_year(self):
        # This method can either return the current Nepali year from the system, 
        # or you can calculate it based on the current date using a Nepali date conversion library
        # For simplicity, we'll return a static value as an example (e.g., 2081)
        
        # Assuming the current Nepali year is 2081, replace it with actual calculation if necessary
        nepali_year = nepali_datetime.date.today().strftime("%Y")
        return str(nepali_year)

    def get_totals_for_report(self, report):
        # Get all totals for the given MonthlySalaryReport instance
        totals_data = Total.objects.filter(monthlysalary=report)

        totals = {}
        for total in totals_data:
            print(total)
            totals[total.name] = str(total.amount)  # Convert amounts to string to match the requested response format

        return totals

    def get_employee_data_for_report(self, report, employee):
        # Get all employees linked to this MonthlySalaryReport
        employee_salaries = EmployeeSalary.objects.filter(monthly_report=report, empID=employee)

        employee_data_list = []
        for employee in employee_salaries:
            # Get pay packages for the employee
            paypackages = EmployeeSalaryPayPackage.objects.filter(employee=employee)
            paypackage_list = []
            for package in paypackages:
                paypackage_list.append({
                    "package_name": package.package_name,
                    "amount": str(package.amount),
                    "package_type": "",
                    "taxable": False
                })
            paypackage_list = sorted(paypackage_list, key=lambda x: x['package_name'])
            # Get leave deductions for the employee
            leave_deductions = LeaveDeduction.objects.filter(employee=employee).first()
            leave_deduction_data = {
                "unpaid_leavesdeduction": str(leave_deductions.unpaid_leavesdeduction) if leave_deductions else "0",
                "unpaid_leaves": str(leave_deductions.unpaid_leaves) if leave_deductions else "0"
            }

            # Get fund deductions for the employee
            fund_deductions = FundDeduction.objects.filter(employee=employee)
            fund_deduction_list = []
            for fund in fund_deductions:
                fund_deduction_list.append({
                    "name": fund.name,
                    "amount": str(fund.amount)
                })

            # Get tax deductions for the employee
            tax_deductions = TaxDeduction.objects.filter(employee=employee)
            tax_deduction_list = []
            for tax in tax_deductions:
                tax_deduction_list.append({
                    "name": tax.name,
                    "Total": str(tax.total)
                })

            employee_data = {
                "name": employee.name,
                "total_gross_salary": {
                    "paypackages": paypackage_list,
                    "total_salary": str(employee.total_salary)
                },
                "leave_deductions": leave_deduction_data,
                "empID": employee.empID.id,
                "fund_deductions": fund_deduction_list,
                "tax_deduction": tax_deduction_list,
                "net_amount" : employee.net_amount
            }

            employee_data_list.append(employee_data)

        return employee_data_list
        