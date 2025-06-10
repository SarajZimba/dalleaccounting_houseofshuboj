from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounting.models import AccountLedger, AccountSubLedger, TblJournalEntry, TblCrJournalEntry, TblDrJournalEntry, TrackBill, AccountSubLedgerTracking
from api.serializers.journal_entry import JournalEntrySerializer
from django.shortcuts import render

from api.serializers.credit_journal_entry import CreditJournalEntrySerializer  # Import your serializer
from accounting.models import AccountChart
from datetime import date, datetime


from api.views.journal_entry import check_outlet_subledger


from accounting.utils import update_cumulative_ledger_journal, create_cumulative_ledger_journal
class CreditJournalEntryAPIView(APIView):


    def post(self, request):
        entry_date = date.today()
        entry_datetime = datetime.now()
        data_list = request.data  # Assuming you receive a list of JSON objects
        response_data = []
        
        for data in data_list:
            serializer = CreditJournalEntrySerializer(data=data)

            if serializer.is_valid():
                data = serializer.validated_data

                print(data)

                # Extract data for debit and credit entries
                debit_ledgers = data['debit_ledgers']
                debit_ledger_names = data['debit_ledger_names']
                ledger = debit_ledger_names[0]
                debit_particulars = data['debit_particulars']
                debit_amounts = data['debit_amounts']

                credit_ledgers = data['credit_ledgers']
                credit_particulars = data['credit_particulars']
                credit_amounts = data['credit_amounts']
                posted_datetime = data['datetime']
                bill_no = data['bill_id']
                username = data['user']
                outlet_name = data['outlet_name']
                
                try:
                    outlet_subledger = check_outlet_subledger(outlet_name)
                except Exception as e:
                    return Response({'message': 'Error occured while creating the outlet subledger'}, 400)

                try:
                    sundry_debtors_object = AccountChart.objects.get(group="Sundry Debtors")
                except AccountChart.DoesNotExist:
                    sundry_debtors_object = None                

                # Validate amounts
                try:
                    parsed_debitamt = [Decimal(i) for i in debit_amounts]
                    parsed_creditamt = [Decimal(i) for i in credit_amounts]
                except Exception:
                    response_data.append({'message': 'Please Enter a valid amount'})
                    continue  # Skip this entry and move to the next one

                debit_sum, credit_sum = sum(parsed_debitamt), sum(parsed_creditamt)

                if len(debit_ledgers) != len(debit_particulars):
                    response_data.append({'message': 'Number of Debit Ledgers and Debit Particulars must be the same'})
                    continue  # Skip this entry and move to the next one

                # Validate that the lengths of credit_particulars and credit_subledgers match
                if len(credit_ledgers) != len(credit_particulars):
                    response_data.append({'message': 'Number of Credit Ledgers and Credit Particulars must be the same'})
                    continue 

                # Validate that debit and credit totals are equal
                if debit_sum != credit_sum:
                    response_data.append({'message': 'Debit Total and Credit Total must be equal'})
                    continue  # Skip this entry and move to the next one
                i = 0
                # Validate debit and credit ledgers
                for dr in debit_ledgers:
                    if dr.startswith('-'):
                        response_data.append({'message': 'Ledger must be selected'})
                        continue  # Skip this entry and move to the next one
                    
                    if debit_ledger_names[i] ==  "Discount Expenses":
                        continue # Skip this entry and move to the next one

                    if not AccountLedger.objects.filter(idcredit=dr).exists():
                        # debit_ledger_names = data.get("debit_ledger_names", [])[0] if data.get("debit_ledger_names") else None
                        AccountLedger.objects.create(idcredit=dr, ledger_name=ledger, account_chart=sundry_debtors_object)
                    i = i + 1

                for cr in credit_ledgers:
                    if cr.startswith('-'):
                        response_data.append({'message': 'Ledger must be selected'})
                        continue  # Skip this entry and move to the next one

                    if not AccountLedger.objects.filter(pk=cr).exists():
                        response_data.append({'message': 'There is no credit_ledger of that id in the database'})
                        continue  # Skip this entry and move to the next one



                if TrackBill.objects.filter(datetime=posted_datetime, bill=bill_no).exists():
                    response_data.append({'message': 'Entry with the same datetime and bill number already exists'})
                    continue
                
                else:
                    TrackBill.objects.create(datetime=posted_datetime, bill=bill_no)

                credit_to_debit_mapping = {}

                # Create a journal entry
                journal_entry = TblJournalEntry.objects.create(employee_name=username, journal_total=debit_sum, entry_date=entry_date)

                # Process credit entries
                for i in range(len(credit_ledgers)):
                    credit_ledger_id = int(credit_ledgers[i])
                    credit_ledger = AccountLedger.objects.get(pk=credit_ledger_id)
                    credit_particular = credit_particulars[i]
                    credit_amount = parsed_creditamt[i]
                    credit_ledger_type = credit_ledger.account_chart.account_type
                    # TblCrJournalEntry.objects.create(ledger=credit_ledger, journal_entry=journal_entry, particulars=credit_particular, credit_amount=credit_amount)
                    if credit_ledger.ledger_name == "Sales":                    
                        TblCrJournalEntry.objects.create(ledger=credit_ledger, journal_entry=journal_entry, particulars=credit_particular, credit_amount=credit_amount, sub_ledger=outlet_subledger)
                    else:
                        TblCrJournalEntry.objects.create(ledger=credit_ledger, journal_entry=journal_entry, particulars=credit_particular, credit_amount=credit_amount) 

                    # Update ledger and subledger totals
                    if credit_ledger_type in ['Asset', 'Expense']:
                        credit_ledger.total_value = credit_ledger.total_value - credit_amount
                        credit_ledger.save()
                        create_cumulative_ledger_journal(credit_ledger, journal_entry, entry_datetime)
                    elif credit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                        credit_ledger.total_value = credit_ledger.total_value + credit_amount
                        credit_ledger.save()
                        create_cumulative_ledger_journal(credit_ledger, journal_entry, entry_datetime)
                        
                        if credit_ledger.ledger_name == "Sales":
                            prev_value = outlet_subledger.total_value
                            subledgertracking = AccountSubLedgerTracking.objects.create(subledger = outlet_subledger, prev_amount= prev_value, journal=journal_entry)

                            outlet_subledger.total_value = outlet_subledger.total_value + credit_amount
                            outlet_subledger.save()
                            subledgertracking.new_amount=outlet_subledger.total_value
                            subledgertracking.value_changed = outlet_subledger.total_value - prev_value
                            subledgertracking.save()

                # Process debit entries
                for i in range(len(debit_ledgers)):
                    
                    if debit_ledger_names[i] == "Discount Expenses":
                        discount_expense_ledger = AccountLedger.objects.get(ledger_name = "Discount Expenses")
                        debit_particular = debit_particulars[i]
                        debit_amount = parsed_debitamt[i]
                        debit_ledger_type = discount_expense_ledger.account_chart.account_type                        
                        
                        TblDrJournalEntry.objects.create(ledger=discount_expense_ledger, journal_entry=journal_entry, particulars=debit_particular, debit_amount=debit_amount, paidfrom_ledger=credit_to_debit_mapping.get(credit_ledger))
                        # Update ledger and subledger totals

                        if debit_ledger_type in ['Asset', 'Expense']:
                            discount_expense_ledger.total_value = discount_expense_ledger.total_value + debit_amount
                            discount_expense_ledger.save()
                            create_cumulative_ledger_journal(discount_expense_ledger, journal_entry, entry_datetime)
                        elif debit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                            discount_expense_ledger.total_value = discount_expense_ledger.total_value - debit_amount
                            discount_expense_ledger.save()
                            create_cumulative_ledger_journal(discount_expense_ledger, journal_entry, entry_datetime)   
                            

                    else:    
                        debit_ledger_id = debit_ledgers[i]
                        debit_ledger = AccountLedger.objects.get(idcredit=debit_ledger_id)
                        debit_particular = debit_particulars[i]
                        debit_amount = parsed_debitamt[i]
                        debit_ledger_type = debit_ledger.account_chart.account_type
                        TblDrJournalEntry.objects.create(ledger=debit_ledger, journal_entry=journal_entry, particulars=debit_particular, debit_amount=debit_amount, paidfrom_ledger=credit_to_debit_mapping.get(credit_ledger))
    
                        # Update ledger and subledger totals
                        if debit_ledger_type in ['Asset', 'Expense']:
                            debit_ledger.total_value = debit_ledger.total_value + debit_amount
                            debit_ledger.save()
                            create_cumulative_ledger_journal(debit_ledger, journal_entry, entry_datetime)
                        elif debit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                            debit_ledger.total_value = debit_ledger.total_value - debit_amount
                            debit_ledger.save()
                            create_cumulative_ledger_journal(debit_ledger, journal_entry, entry_datetime)

                response_data.append({'message': 'Journal entry created successfully'})

            else:
                response_data.append({'error': serializer.errors}, 400)


        return Response(response_data, status=status.HTTP_201_CREATED)