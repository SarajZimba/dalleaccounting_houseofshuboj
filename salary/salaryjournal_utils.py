from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounting.models import AccountSubLedgerTracking
from accounting.utils import change_date_to_datetime
from accounting.models import AccountLedger, AccountSubLedger, AccountChart, TblJournalEntry, TblCrJournalEntry, TblDrJournalEntry, TrackBill
from decimal import Decimal as D

from accounting.utils import update_cumulative_ledger_journal, create_cumulative_ledger_journal, change_date_to_datetime
from rest_framework.response import Response

from datetime import datetime




def get_subledger(subledger, ledger):
    subled = None
    if not subledger.startswith('-'):
        try:
            subledger_id = int(subledger)
            subled = AccountSubLedger.objects.get(pk=subledger_id)
        except ValueError:
            subled = AccountSubLedger.objects.create(sub_ledger_name=subledger, is_editable=True, ledger=ledger)
    return subled

def salaryjournalentry(data):
    posted_data = data

    
    print(f"posted data in salaryjournal {posted_data}")
    posted_employees_data = posted_data["response_list"]
    salary_name = "Salary Expenses"

    try:
        salary_ledger = AccountLedger.objects.get(ledger_name=salary_name)
    except AccountLedger.DoesNotExist:
        salary_ledger = AccountLedger.objects.create(ledger_name=salary_name)
    posted_paidfromledger = posted_data["ledger_id"]
    posted_paidfromsubledger = posted_data["subledger_id"]
    paid_from_ledger = AccountLedger.objects.get(id=int(posted_paidfromledger))
    if posted_paidfromsubledger:
        paid_from_subledger = AccountSubLedger.objects.get(id=int(posted_paidfromsubledger))

    # paid_from_ledger_name = "Bank Accounts"

    # paid_from_subledger_name = "Himalayan Bank"

    # try:
    #     paid_from_ledger = AccountLedger.objects.get(ledger_name=paid_from_ledger_name)
    # except AccountLedger.DoesNotExist:
    #     paid_from_ledger = AccountLedger.objects.create(ledger_name=paid_from_ledger_name)

    paid_from_ledger_particular = "To " + paid_from_ledger.ledger_name 
    # try:
    #     paid_from_subledger = AccountSubLedger.objects.get(sub_ledger_name=paid_from_subledger_name, ledger=paid_from_ledger)
    # except AccountSubLedger.DoesNotExist:
    #     paid_from_subledger = AccountSubLedger.objects.create(sub_ledger_name=paid_from_subledger_name, ledger=paid_from_ledger)

    for data in posted_employees_data:
        total_salary = data["total_gross_salary"]["total_salary"]
        employee_name = data["name"]
        fund_deductions = data["fund_deductions"]
        tax_deductions = data["tax_deduction"]

        fund_deduction_name = ""
        fund_deduction_total = 0.0

        netsalary_total = data["net_amount"]
        for fund_deduction in fund_deductions:

            if fund_deduction["name"] == "Social Security Fund":
                fund_deduction_name = fund_deduction["name"]
                fund_deduction_total = fund_deduction["amount"]
                break
            if fund_deduction["name"] == "Employees Provident Fund":
                fund_deduction_name = fund_deduction["name"]
                fund_deduction_total = fund_deduction["amount"]
                break


        try:
            fund_deduction_ledger = AccountLedger.objects.get(ledger_name=fund_deduction_name)
        except AccountLedger.DoesNotExist:
            fund_deduction_ledger = AccountLedger.objects.create(ledger_name=fund_deduction_name)

        fund_deduction_subledger_name  = employee_name + "-" + fund_deduction_name
        try:

            fund_deduction_subledger = AccountSubLedger.objects.get(sub_ledger_name=fund_deduction_subledger_name, ledger=fund_deduction_ledger)  
        except AccountSubLedger.DoesNotExist:
            fund_deduction_subledger = AccountSubLedger.objects.create(sub_ledger_name=fund_deduction_subledger_name, ledger=fund_deduction_ledger)                
            
        salary_subledger_name  = employee_name + "-" + salary_name
        try:

            salary_subledger = AccountSubLedger.objects.get(sub_ledger_name=salary_subledger_name, ledger=salary_ledger)  
        except AccountSubLedger.DoesNotExist:
            salary_subledger = AccountSubLedger.objects.create(sub_ledger_name=salary_subledger_name, ledger=salary_ledger)                

        tax_name = ""
        tax_total = 0.0
        for tax in tax_deductions:

            if tax["name"] == "Total Tax":
                tax_name = tax["name"]
                tax_total = tax["Total"]
                break

        vat_ledger_name = "Income Tax"
        try:
            vat_ledger = AccountLedger.objects.get(ledger_name=vat_ledger_name)
        except AccountLedger.DoesNotExist:
            vat_ledger = AccountLedger.objects.create(ledger_name=vat_ledger_name)

        vat_ledger_subledger_name  = employee_name + "-" + tax_name
        try:

            vat_subledger = AccountSubLedger.objects.get(sub_ledger_name=vat_ledger_subledger_name, ledger=vat_ledger)  
        except AccountSubLedger.DoesNotExist:
            vat_subledger = AccountSubLedger.objects.create(sub_ledger_name=vat_ledger_subledger_name, ledger=vat_ledger)                
            

        fund_deduction_particular = fund_deduction_name + " a/c Dr"
        salary_particular = salary_name + " a/c Dr"
        tax_particular = vat_ledger_name + " a/c Dr"
        tax_ledger = vat_ledger


        debit_ledgers = []
        debit_ledgers.append(str(fund_deduction_ledger.id))
        debit_ledgers.append(str(salary_ledger.id) )
        debit_ledgers.append(str(tax_ledger.id))
        debit_particulars = []
        debit_particulars.append(fund_deduction_particular)
        debit_particulars.append(salary_particular)
        debit_particulars.append(tax_particular)
        debit_amounts = []
        debit_amounts.append(fund_deduction_total)
        debit_amounts.append(netsalary_total)
        debit_amounts.append(tax_total)
        debit_subledgers = []

        debit_subledgers.append(str(fund_deduction_subledger.id))
        debit_subledgers.append(str(salary_subledger.id))
        debit_subledgers.append(str(vat_subledger.id))

        credit_ledgers = []

        credit_ledgers.append(str(paid_from_ledger.id))

        credit_particulars = []
        credit_particulars.append(paid_from_ledger_particular)
        credit_amounts = []
        credit_amounts.append(str(total_salary))
        credit_subledgers = []
        if posted_paidfromsubledger:
            credit_subledgers.append(str(paid_from_subledger.id))
            # print(credit_ledgers)
        else:
            # -----
            credit_subledgers.append(str('-----'))
        entry_date = datetime.today().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
        print(f"before calling function {entry_date}")
        entry_datetime_for_cumulativeledger = change_date_to_datetime(entry_date)
        narration = ''
        ledgers = AccountLedger.objects.all()
        sub_ledgers = AccountSubLedger.objects.all()

        credit_to_debit_mapping = {}

        journal_entry = TblJournalEntry.objects.create(employee_name="HR", journal_total=total_salary,  entry_date=entry_date, narration=narration)
        for i in range(len(credit_ledgers)):
            credit_ledger_id = int(credit_ledgers[i])
                
            credit_ledger = AccountLedger.objects.get(pk=credit_ledger_id)
            
            credit_to_debit_mapping[credit_ledger] = credit_ledger
            credit_particular = credit_particulars[i]
            credit_amount = D(credit_amounts[i])
            subledger = get_subledger(credit_subledgers[i], credit_ledger)
            credit_ledger_type = credit_ledger.account_chart.account_type
            TblCrJournalEntry.objects.create(ledger=credit_ledger, journal_entry=journal_entry, particulars=credit_particular, credit_amount=credit_amount, sub_ledger=subledger, paidfrom_ledger=credit_ledger)
            if credit_ledger_type in ['Asset', 'Expense']:
                credit_ledger.total_value = credit_ledger.total_value - credit_amount
                credit_ledger.save()
                create_cumulative_ledger_journal(credit_ledger, journal_entry, entry_datetime_for_cumulativeledger)
                    # create_cumulative_ledger_journal(credit_ledger)
                if subledger:
                    prev_value = subledger.total_value
                    subledgertracking = AccountSubLedgerTracking.objects.create(subledger = subledger, prev_amount= prev_value, journal=journal_entry )

                    subledger.total_value = subledger.total_value - credit_amount
                    subledger.save()
                    subledgertracking.new_amount=subledger.total_value
                    subledgertracking.value_changed = subledger.total_value - prev_value
                    subledgertracking.save()
            elif credit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                credit_ledger.total_value = credit_ledger.total_value + credit_amount
                credit_ledger.save()
                create_cumulative_ledger_journal(credit_ledger, journal_entry, entry_datetime_for_cumulativeledger)
                # create_cumulative_ledger_journal(credit_ledger)
                if subledger:
                    prev_value = subledger.total_value
                    subledgertracking = AccountSubLedgerTracking.objects.create(subledger = subledger, prev_amount= prev_value, journal=journal_entry)

                    subledger.total_value = subledger.total_value + credit_amount
                    subledger.save()
                    subledgertracking.new_amount=subledger.total_value
                    subledgertracking.value_changed = subledger.total_value - prev_value
                    subledgertracking.save()

            
        for i in range(len(debit_ledgers)):
            debit_ledger_id = int(debit_ledgers[i])
            debit_ledger = AccountLedger.objects.get(pk=debit_ledger_id)
            debit_particular = debit_particulars[i]
            debit_amount = D(debit_amounts[i])
            subledger = get_subledger(debit_subledgers[i], debit_ledger)
            debit_ledger_type = debit_ledger.account_chart.account_type
            TblDrJournalEntry.objects.create(ledger=debit_ledger, journal_entry=journal_entry, particulars=debit_particular, debit_amount=debit_amount, sub_ledger=subledger, paidfrom_ledger=credit_to_debit_mapping.get(credit_ledger))
            if debit_ledger_type in ['Asset', 'Expense']:
                debit_ledger.total_value = debit_ledger.total_value + debit_amount
                debit_ledger.save()
                create_cumulative_ledger_journal(debit_ledger, journal_entry, entry_datetime_for_cumulativeledger)
                # create_cumulative_ledger_journal(debit_ledger)
                if subledger:
                    prev_value = subledger.total_value
                    subledgertracking = AccountSubLedgerTracking.objects.create(subledger = subledger, prev_amount= prev_value, journal=journal_entry)

                    subledger.total_value = subledger.total_value + debit_amount
                    subledger.save()
                    subledgertracking.new_amount=subledger.total_value
                    subledgertracking.value_changed = subledger.total_value - prev_value
                    subledgertracking.save()
            elif debit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                debit_ledger.total_value = debit_ledger.total_value - debit_amount
                debit_ledger.save()
                create_cumulative_ledger_journal(debit_ledger, journal_entry, entry_datetime_for_cumulativeledger)
                if subledger:
                    prev_value = subledger.total_value
                    subledgertracking = AccountSubLedgerTracking.objects.create(subledger = subledger, prev_amount= prev_value, journal=journal_entry)

                    subledger.total_value = subledger.total_value - debit_amount
                    subledger.save()
                    subledgertracking.new_amount=subledger.total_value
                    subledgertracking.value_changed = subledger.total_value - prev_value
                    subledgertracking.save()
        print("salary journal created")
    return Response({"detail":"Salary Journal Created Successfully" }, 200)