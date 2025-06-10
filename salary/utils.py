# def calculate_tax(monthly_salary, sst_deduct):
#     yearly_salary = round(float(monthly_salary) * 12, 2)

#     # Define tax slabs and rates
#     tax_slabs = [
#         # (500000, 0.01),   # 1% for the first 500,000
#         (200000, 0.10),   # 10% for the next 200,000
#         (300000, 0.20),   # 20% for the next 300,000
#         (1000000, 0.30),  # 30% for the next 1,000,000
#         (3000000, 0.36),  # 36% for the next 3,000,000
#     ]
#     high_rate = 0.39  # Above 5,000,000 at 39%

#     # Initial tax amounts
#     sst = 0.0
#     remunerable_tax = 0.0

#     if yearly_salary <= 500000:

#         if sst_deduct == "sst_deduct_true":
#             # return {"sst": round((float(yearly_salary)*0.01)/12, 2), "remunerable_tax": 0.0, "total_tax": 0.0}
        
#             data = [
#                 {"name": "sst",  "total": round((float(yearly_salary)*0.01)/12, 2)},
#                 {"name": "remunerable_tax",  "total": 0.0},
#                 {"name": "total_tax",  "total": round((float(yearly_salary)*0.01)/12, 2)},
#             ]

#             return data
#         if sst_deduct == "sst_deduct_false":
#             # return {"sst": (float(0.0)), "remunerable_tax": 0.0, "total_tax": 0.0}    
#             data = [
#                 {"name": "sst",  "total": 0.0},
#                 {"name": "remunerable_tax",  "total": 0.0},
#                 {"name": "total_tax",  "total": 0.0},
#             ]       
#     remaining_salary = yearly_salary

#     # First Rs. 500,000 taxed at 1%, store in ssf
#     if remaining_salary > 500000:
#         if sst_deduct == "sst_deduct_true":
#             sst = round(5000/12, 2)  # Fixed tax for first slab
#         if sst_deduct == "sst_deduct_false":
#             sst = 0.0  # Fixed tax for first slab in case of ssf
#         remaining_salary -= 500000

#     # Apply progressive tax on remaining salary
#     for slab_limit, rate in tax_slabs:
#         if remaining_salary <= 0:
#             break

#         taxable_amount = min(remaining_salary, slab_limit)
#         tax = taxable_amount * rate
#         remunerable_tax += tax
#         remaining_salary -= taxable_amount

#     # If salary exceeds Rs. 5,000,000, apply 39% on the rest
#     if remaining_salary > 0:
#         remunerable_tax += remaining_salary * high_rate

#     remunerable_tax = round(float(remunerable_tax)/12, 2)

#     total_tax = sst + remunerable_tax

#     # return {
#     #     "sst": sst,
#     #     "remunerable_tax": remunerable_tax,
#     #     "total_tax": total_tax
#     # }


#     deduction_list = []

#     sst_data = {"name":"sst", "total":sst}
#     # renumerable_data = {"name":"renumerable_tax", "total": round(float(remunerable_tax)/12, 2)}
#     renumerable_data = {"name":"renumerable_tax", "total": round(float(remunerable_tax), 2)}
#     # total_data = {"name":"total_tax", "total": round(float(total_tax)/12, 2)}
#     total_data = {"name":"total_tax", "total": round(float(total_tax), 2)}

#     deduction_list.append(sst_data)
#     deduction_list.append(renumerable_data)
#     deduction_list.append(total_data)
#     # return {
#     #     "sst": sst,
#     #     "remunerable_tax": remunerable_tax,
#     #     "total_tax": total_tax
#     # }

#     return deduction_list


# def calculate_net_salary(total_amount, tax_deduction):
#     # print(tax_deduction)
#     for item in tax_deduction:
#         print(item)
#         if item["name"] == "total_tax":
#             total_tax = item["total"]
#             break

#     net_amount = total_amount - Decimal(total_tax)
#     # net_amount = 0.0

#     return net_amount

def calculate_tax(monthly_salary, sst_deduct):
    yearly_salary = round(float(monthly_salary) * 12, 2)

    # Define tax slabs and rates
    tax_slabs = [
        # (500000, 0.01),   # 1% for the first 500,000
        (200000, 0.10),   # 10% for the next 200,000
        (300000, 0.20),   # 20% for the next 300,000
        (1000000, 0.30),  # 30% for the next 1,000,000
        (3000000, 0.36),  # 36% for the next 3,000,000
    ]
    high_rate = 0.39  # Above 5,000,000 at 39%

    # Initial tax amounts
    sst = 0.0
    income_tax = 0.0

    if yearly_salary <= 500000:

        if sst_deduct == "sst_deduct_true":
            # return {"sst": round((float(yearly_salary)*0.01)/12, 2), "income_tax": 0.0, "total_tax": 0.0}
        
            data = [
                {"name": "SST",  "Total": round((float(yearly_salary)*0.01)/12, 2)},
                {"name": "Income Tax",  "Total": 0.0},
                {"name": "Total Tax",  "Total": round((float(yearly_salary)*0.01)/12, 2)},
            ]

            return data
        if sst_deduct == "sst_deduct_false":
            # return {"sst": (float(0.0)), "income_tax": 0.0, "total_tax": 0.0}    
            data = [
                {"name": "SST",  "Total": 0.0},
                {"name": "Income Tax",  "Total": 0.0},
                {"name": "Total Tax",  "Total": 0.0},
            ]  
            return data
    remaining_salary = yearly_salary

    # First Rs. 500,000 taxed at 1%, store in ssf
    if remaining_salary > 500000:
        if sst_deduct == "sst_deduct_true":
            sst = round(5000/12, 2)  # Fixed tax for first slab
        if sst_deduct == "sst_deduct_false":
            sst = 0.0  # Fixed tax for first slab in case of ssf
        remaining_salary -= 500000

    # Apply progressive tax on remaining salary
    for slab_limit, rate in tax_slabs:
        if remaining_salary <= 0:
            break

        taxable_amount = min(remaining_salary, slab_limit)
        tax = taxable_amount * rate
        income_tax += tax
        remaining_salary -= taxable_amount

    # If salary exceeds Rs. 5,000,000, apply 39% on the rest
    if remaining_salary > 0:
        income_tax += remaining_salary * high_rate

    income_tax = round(float(income_tax)/12, 2)

    total_tax = sst + income_tax

    # return {
    #     "sst": sst,
    #     "income_tax": income_tax,
    #     "total_tax": total_tax
    # }


    deduction_list = []

    sst_data = {"name":"SST", "Total":sst}
    # renumerable_data = {"name":"renumerable_tax", "total": round(float(income_tax)/12, 2)}
    renumerable_data = {"name":"Income Tax", "Total": round(float(income_tax), 2)}
    # total_data = {"name":"total_tax", "total": round(float(total_tax)/12, 2)}
    total_data = {"name":"Total Tax", "Total": round(float(total_tax), 2)}

    deduction_list.append(sst_data)
    deduction_list.append(renumerable_data)
    deduction_list.append(total_data)
    # return {
    #     "sst": sst,
    #     "income_tax": income_tax,
    #     "total_tax": total_tax
    # }

    return deduction_list


# def calculate_tax(monthly_salary, sst_deduct):
#     yearly_salary = round(float(monthly_salary) * 12, 2)

#     # Define tax slabs and rates
#     tax_slabs = [
#         # (500000, 0.01),   # 1% for the first 500,000
#         (200000, 0.10),   # 10% for the next 200,000
#         (300000, 0.20),   # 20% for the next 300,000
#         (1000000, 0.30),  # 30% for the next 1,000,000
#         (3000000, 0.36),  # 36% for the next 3,000,000
#     ]
#     high_rate = 0.39  # Above 5,000,000 at 39%

#     # Initial tax amounts
#     sst = 0.0
#     remunerable_tax = 0.0

#     if yearly_salary <= 500000:

#         if sst_deduct == "sst_deduct_true":
#             # return {"sst": round((float(yearly_salary)*0.01)/12, 2), "remunerable_tax": 0.0, "total_tax": 0.0}
        
#             data = [
#                 {"name": "SST",  "Total": round((float(yearly_salary)*0.01)/12, 2)},
#                 {"name": "Remunerable Tax",  "Total": 0.0},
#                 {"name": "Total Tax",  "Total": round((float(yearly_salary)*0.01)/12, 2)},
#             ]

#             return data
#         if sst_deduct == "sst_deduct_false":
#             # return {"sst": (float(0.0)), "remunerable_tax": 0.0, "total_tax": 0.0}    
#             data = [
#                 {"name": "SST",  "Total": 0.0},
#                 {"name": "Remunerable Tax",  "Total": 0.0},
#                 {"name": "Total Tax",  "Total": 0.0},
#             ]       
#     remaining_salary = yearly_salary

#     # First Rs. 500,000 taxed at 1%, store in ssf
#     if remaining_salary > 500000:
#         if sst_deduct == "sst_deduct_true":
#             sst = round(5000/12, 2)  # Fixed tax for first slab
#         if sst_deduct == "sst_deduct_false":
#             sst = 0.0  # Fixed tax for first slab in case of ssf
#         remaining_salary -= 500000

#     # Apply progressive tax on remaining salary
#     for slab_limit, rate in tax_slabs:
#         if remaining_salary <= 0:
#             break

#         taxable_amount = min(remaining_salary, slab_limit)
#         tax = taxable_amount * rate
#         remunerable_tax += tax
#         remaining_salary -= taxable_amount

#     # If salary exceeds Rs. 5,000,000, apply 39% on the rest
#     if remaining_salary > 0:
#         remunerable_tax += remaining_salary * high_rate

#     remunerable_tax = round(float(remunerable_tax)/12, 2)

#     total_tax = sst + remunerable_tax

#     # return {
#     #     "sst": sst,
#     #     "remunerable_tax": remunerable_tax,
#     #     "total_tax": total_tax
#     # }


#     deduction_list = []

#     sst_data = {"name":"SST", "Total":sst}
#     # renumerable_data = {"name":"renumerable_tax", "total": round(float(remunerable_tax)/12, 2)}
#     renumerable_data = {"name":"Renumerable Tax", "Total": round(float(remunerable_tax), 2)}
#     # total_data = {"name":"total_tax", "total": round(float(total_tax)/12, 2)}
#     total_data = {"name":"Total Tax", "Total": round(float(total_tax), 2)}

#     deduction_list.append(sst_data)
#     deduction_list.append(renumerable_data)
#     deduction_list.append(total_data)
#     # return {
#     #     "sst": sst,
#     #     "remunerable_tax": remunerable_tax,
#     #     "total_tax": total_tax
#     # }

#     return deduction_list


def calculate_net_salary(total_amount, tax_deduction):
    for item in tax_deduction:
        if item["name"] == "Total Tax":
            total_tax = item["Total"]
            break

    net_amount = total_amount - Decimal(total_tax)
    # net_amount = 0.0

    return net_amount

from decimal import Decimal

def calculate_totals(employee_data):
    totals = {}
    
    # Iterate over each employee data
    for employee in employee_data:
        # Sum up pay packages dynamically
        # for package in employee.get("total_gross_salary", {}).get("paypackages", []):
        #     package_name = package["package_name"]
        #     totals[package_name] = totals.get(package_name, Decimal(0.0)) + package["amount"]
        
        # Sum total salary
        totals["total_salary"] = totals.get("total_salary", Decimal(0.0)) + employee.get("total_gross_salary", {}).get("total_salary", Decimal(0.0))
        
        # Sum net amount
        totals["net_amount"] = totals.get("net_amount", Decimal(0.0)) + employee.get("net_amount", Decimal(0.0))
        
        # # Sum up fund deductions dynamically
        # for deduction in employee.get("fund_deductions", []):
        #     deduction_name = deduction["name"]
        #     totals[deduction_name] = totals.get(deduction_name, Decimal(0.0)) + deduction["amount"]
        
        # Sum up tax deductions dynamically
        for tax in employee.get("tax_deduction", []):
            # tax_name = tax["name"].lower()  # Normalize the tax name to lowercase for consistency
            tax_name = tax["name"]  # Normalize the tax name to lowercase for consistency
            totals[tax_name] = totals.get(tax_name, Decimal(0.0)) + Decimal(tax["Total"])
    
    return totals


import nepali_datetime
def get_nepali_date():

    # Get today's Nepali date
    today_nepali = nepali_datetime.date.today().strftime("%d %B %Y")
    # Get Nepali month and date
    nepali_month = nepali_datetime.date.today().strftime("%B")

    return nepali_month, today_nepali