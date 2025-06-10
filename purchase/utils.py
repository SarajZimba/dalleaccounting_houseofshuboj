# from accounting.models import CumulativeLedger
# from decimal import Decimal


# """
# Signal to update Cumulative Ledger
# """
# from datetime import date
# def update_cumulative_ledger_purchase(instance, entry_date):
#     ledger = CumulativeLedger.objects.filter(ledger=instance).last()
#     if ledger :
#         total_value = ledger.total_value
#     else:
#         total_value = Decimal(0.0)
#     value_changed = instance.total_value - total_value
#     if instance.account_chart.account_type in ['Asset', 'Expense']:
#         if value_changed > 0:
#                 CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, debit_amount=abs(value_changed), ledger=instance, entry_date=entry_date)
#         else:
#             CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, credit_amount=abs(value_changed), ledger=instance, entry_date=entry_date)
#     else:
#         if value_changed > 0:
#             CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, credit_amount=abs(value_changed), ledger=instance, entry_date=entry_date)
#         else:
#             CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, debit_amount=abs(value_changed), ledger=instance, entry_date=entry_date)

# def create_cumulative_ledger_purchase(instance, entry_date):
#     if instance.account_chart.account_type in ['Asset', 'Expense']:
#         CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=instance.total_value, ledger=instance, debit_amount=instance.total_value, entry_date=entry_date)
#     else:
#         CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=instance.total_value, ledger=instance, credit_amount=instance.total_value, entry_date=entry_date)

from accounting.models import CumulativeLedger
from decimal import Decimal


"""
Signal to update Cumulative Ledger
"""
from datetime import date
def update_cumulative_ledger_purchase(instance, entry_date, journal_entry):
    ledger = CumulativeLedger.objects.filter(ledger=instance).last()
    if ledger :
        total_value = ledger.total_value
    else:
        total_value = Decimal(0.0)
    value_changed = instance.total_value - total_value
    if instance.account_chart.account_type in ['Asset', 'Expense']:
        if value_changed > 0:
                CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, debit_amount=abs(value_changed), ledger=instance, entry_date=entry_date, journal=journal_entry)
        else:
            CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, credit_amount=abs(value_changed), ledger=instance, entry_date=entry_date, journal=journal_entry)
    else:
        if value_changed > 0:
            CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, credit_amount=abs(value_changed), ledger=instance, entry_date=entry_date,  journal=journal_entry)
        else:
            CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=value_changed, debit_amount=abs(value_changed), ledger=instance, entry_date=entry_date,  journal=journal_entry)

def create_cumulative_ledger_purchase(instance, entry_date, journal_entry):
    if instance.account_chart.account_type in ['Asset', 'Expense']:
        CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=instance.total_value, ledger=instance, debit_amount=instance.total_value, entry_date=entry_date, journal=journal_entry)
    else:
        CumulativeLedger.objects.create(account_chart=instance.account_chart, ledger_name=instance.ledger_name, total_value=instance.total_value, value_changed=instance.total_value, ledger=instance, credit_amount=instance.total_value, entry_date=entry_date, journal=journal_entry)
