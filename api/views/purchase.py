from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounting.models import AccountSubLedgerTracking
from accounting.utils import change_date_to_datetime

import decimal
from decimal import Decimal
from accounting.models import AccountLedger, AccountSubLedger, AccountChart, TblJournalEntry, TblCrJournalEntry, TblDrJournalEntry, TrackBill
# from bill.utils import create_cumulative_ledger_bill, update_cumulative_ledger_bill
from purchase.utils import create_cumulative_ledger_purchase, update_cumulative_ledger_purchase
from purchase.models import Purchase, ProductPurchase, TblpurchaseEntry, Vendor
from num2words import num2words
import json


from product.models import Product, ProductCategory

def amountinwords(amount):
    rupees = int(amount)
    paisa = round((amount - rupees) * 100)  # Convert decimal part to paisa

    # Convert rupees to words
    rupees_words = num2words(rupees, lang='en_IN') + " rupees"

    # Convert paisa to words if it's not zero
    paisa_words = ""
    if paisa > 0:
        paisa_words = " and " + num2words(paisa, lang='en_IN') + " paisa"

    return rupees_words + paisa_words

from datetime import datetime
class CreatePurchaseAPIView(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data
        print(data)
        bill_no = data.get('purchaseBillNumber', None)
        received_date = data.get('ReceivedDate', None)
        if received_date:
            # Convert string to datetime object
            bill_date = datetime.strptime(received_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
        else:
            bill_date = None
        pp_no = data.get('pp_no',None)
        vendor_name = data.get('Company_Name')
        grand_total = data.get('TotalAmount')
        discount_percentage = data.get('discount_percentage', 0)
        discount_amount = data.get('DiscountAmount')
        tax_amount = data.get('TaxAmount', 0)
        grn = data.get('GRN', None)
        sub_total = grand_total - tax_amount + discount_amount

        taxable_amount = 0
        non_taxable_amount = 0
        if tax_amount == 0:
            if discount_amount == 0:
                non_taxable_amount = sub_total
            else:
                non_taxable_amount = sub_total - discount_amount
        
        else:
            if discount_amount == 0 :
                taxable_amount = sub_total
            else:
                taxable_amount = sub_total - discount_amount
        # grand_total = sub_total + tax_amount - discount_amount
            
        # grand_total = data.get('grand_total')
        amount_in_words = amountinwords(grand_total)
        payment_mode = data.get('paymentMode')

        debit_account_ledger = AccountLedger.objects.get(ledger_name='Inventory Expenses')
        debit_account = debit_account_ledger.id

        product_lists = data.get("RequisitionDetailsList", [])        
        no_of_items_sent = len(product_lists)


        try:
            vendor_obj = Vendor.objects.get(name = vendor_name)
            vendor_id = vendor_obj.id
            vendor_pan = vendor_obj.pan_no
        except Vendor.DoesNotExist:
            vendor_obj = Vendor.objects.create(name=vendor_name)
            vendor_id = vendor_obj.id
            vendor_pan = vendor_obj.pan_no
        item_name = ''

        total_quantity = 0


        purchase_object = Purchase(
            bill_no=bill_no,
            vendor_id=vendor_id,sub_total=sub_total, bill_date=bill_date,
            discount_percentage=discount_percentage,discount_amount=discount_amount,
            taxable_amount=taxable_amount, non_taxable_amount=non_taxable_amount,
            tax_amount=tax_amount, grand_total=grand_total,
            amount_in_words=amount_in_words, payment_mode=payment_mode, 
            grn=grn
        )
        purchase_object.save()
        
        if product_lists and len(product_lists) > 0:
            
            for product in product_lists :
                try:
                    product_id = int(product.get('ItemID'))

                    total = float(product.get('UnitsOrdered') * product.get('Rate'))
                    
                    quantity = int(product.get('UnitsOrdered'))
                    rate = float(product.get('Rate'))
                    product_name = product.get('Name', '')
                    product_category = product.get('GroupName', '')
                    try:
                        category_obj = ProductCategory.objects.get(title=product_category)
                    except ProductCategory.DoesNotExist:
                        category_obj = ProductCategory.objects.create(title=product_category) 

                    try:
                        prod = Product.objects.get(title=product_name, category= category_obj)
                    except Product.DoesNotExist:
                        prod = Product.objects.create(title=product_name, category = category_obj) 

                    self.create_subledgers(prod, total, debit_account)
                    ProductPurchase.objects.create(product=prod, purchase=purchase_object, quantity=quantity, rate=rate, item_total=total)
                except (ValueError, Product.DoesNotExist, AccountLedger.DoesNotExist):
                    pass

        TblpurchaseEntry.objects.create(
            bill_no=bill_no, bill_date=bill_date, pp_no=pp_no, vendor_name=vendor_name, vendor_pan=vendor_pan,
            item_name=item_name, quantity=total_quantity, amount=grand_total, tax_amount=tax_amount, non_tax_purchase=non_taxable_amount, grn=grn
        )
        vendor_detail = str(vendor_obj.pk)+' '+ vendor_name
        # self.create_accounting(debit_account_id=debit_account, payment_mode=payment_mode, username=self.request.user.username, sub_total=sub_total, tax_amount=tax_amount, vendor=vendor_detail)
        sub_tax = decimal.Decimal(tax_amount)
        fraction_tax = sub_tax/no_of_items_sent
        print(fraction_tax)
        discount = decimal.Decimal(discount_amount)
        fraction_discount = discount/no_of_items_sent
        print(fraction_tax)

        # if product_lists and len(product_lists) > 0:
            
        #     for product in product_lists:
        #         ledger_id = int(debit_account)
        #         total = float(product.get('UnitsOrdered') * product.get('Rate'))
        #         self.create_accounting_multiple_ledger(debit_account_id=ledger_id, payment_mode=payment_mode, username=self.request.user.username, sub_total=total, tax_amount=fraction_tax, vendor=vendor_detail, entry_date=bill_date, fraction_discount=fraction_discount)
        ledger_id = int(debit_account)
        total = sub_total
        purchase_id = purchase_object.id
        self.create_accounting_multiple_ledger(debit_account_id=ledger_id, payment_mode=payment_mode, username=self.request.user.username, sub_total=total, tax_amount=sub_tax, vendor=vendor_detail, entry_date=bill_date, fraction_discount=discount, purchase_id=purchase_id)

        return Response("Purchase Created Successfully", 200)

    def create_subledgers(self, product, item_total, debit_account):
        debit_account = get_object_or_404(AccountLedger, pk=int(debit_account))
        subledgername = f'{product.title} ({product.category.title}) - Purchase'
        try:
            sub = AccountSubLedger.objects.get(sub_ledger_name=subledgername, ledger=debit_account)
            prev_value = sub.total_value
            subledgertracking = AccountSubLedgerTracking.objects.create(subledger = sub, prev_amount= prev_value)
            sub.total_value += decimal.Decimal(item_total)
            sub.save()
            subledgertracking.new_amount=sub.total_value
            subledgertracking.value_changed = sub.total_value - prev_value
            subledgertracking.save()
        except AccountSubLedger.DoesNotExist:
            subledger = AccountSubLedger.objects.create(sub_ledger_name=subledgername, ledger=debit_account, total_value=item_total)
            subledgertracking = AccountSubLedgerTracking.objects.create(subledger=subledger, new_amount=decimal.Decimal(item_total), value_changed=decimal.Decimal(item_total))

    def create_accounting_multiple_ledger(self, debit_account_id, payment_mode:str, username:str, sub_total, tax_amount, vendor, entry_date, fraction_discount, purchase_id):
        sub_total = decimal.Decimal(sub_total)
        tax_amount = decimal.Decimal(tax_amount)
        total_amount =  sub_total+ tax_amount

        discount_amount = decimal.Decimal(fraction_discount)
        cash_ledger = get_object_or_404(AccountLedger, ledger_name='Cash-In-Hand')
        vat_receivable = get_object_or_404(AccountLedger, ledger_name='VAT Receivable')
        discount_expenses = get_object_or_404(AccountLedger, ledger_name='Discount Expenses')
        discount_sales = get_object_or_404(AccountLedger, ledger_name='Discount Sales')
        debit_account = get_object_or_404(AccountLedger, pk=int(debit_account_id))

        if entry_date:

            entry_datetime_for_cumulativeledger = change_date_to_datetime(entry_date)
        else:
            from datetime import datetime
            entry_datetime_for_cumulativeledger = datetime.now()
        
        journal_entry = TblJournalEntry.objects.create(employee_name=username, journal_total = total_amount, entry_date=entry_date, purchase=purchase_id)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Automatic: {debit_account.ledger_name} A/c Dr.", debit_amount=sub_total, ledger=debit_account)
        debit_account.total_value += sub_total
        debit_account.save()
        update_cumulative_ledger_purchase(debit_account, entry_datetime_for_cumulativeledger, journal_entry)
        if tax_amount > 0:
            TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars="Automatic: VAT Receivable A/c Dr.", debit_amount=tax_amount, ledger=vat_receivable)
            vat_receivable.total_value += tax_amount
            vat_receivable.save()
            update_cumulative_ledger_purchase(vat_receivable, entry_datetime_for_cumulativeledger, journal_entry)
        if discount_amount > 0:
            TblDrJournalEntry.objects.create(journal_entry=journal_entry, particulars="Automatic: Discount Expenses A/c Dr.", debit_amount=discount_amount, ledger=discount_expenses)
            discount_expenses.total_value += discount_amount
            discount_expenses.save()
            update_cumulative_ledger_purchase(discount_expenses, entry_datetime_for_cumulativeledger, journal_entry)
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars="Automatic: To Discount Sales", credit_amount=discount_amount, ledger=discount_sales)
            discount_sales.total_value += discount_amount
            discount_sales.save()
            update_cumulative_ledger_purchase(discount_sales, entry_datetime_for_cumulativeledger, journal_entry)
        if payment_mode.lower().strip() == "credit":
            try:
                vendor_ledger = AccountLedger.objects.get(ledger_name=vendor)
                vendor_ledger.total_value += total_amount
                vendor_ledger.save()
                update_cumulative_ledger_purchase(vendor_ledger, entry_datetime_for_cumulativeledger, journal_entry)
            except AccountLedger.DoesNotExist:
                chart = AccountChart.objects.get(group__iexact='Sundry Creditors')
                vendor_ledger = AccountLedger.objects.create(ledger_name=vendor, total_value=total_amount, is_editable=True, account_chart=chart)
                create_cumulative_ledger_purchase(vendor_ledger, entry_datetime_for_cumulativeledger, journal_entry)
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Automatic: To {vendor_ledger.ledger_name} A/c", credit_amount=total_amount, ledger=vendor_ledger)
        else:
            TblCrJournalEntry.objects.create(journal_entry=journal_entry, particulars=f"Automatic: To {cash_ledger.ledger_name} A/c", credit_amount=total_amount, ledger=cash_ledger)
            cash_ledger.total_value -= total_amount
            cash_ledger.save()
            update_cumulative_ledger_purchase(cash_ledger, entry_datetime_for_cumulativeledger, journal_entry)
            

from accounting.utils import adjust_cumulative_ledger_afterentries
def delete_journal(journal_id):
    try:
        # Retrieve the journal entry or return a 404 if it doesn't exist
        journal_entry = get_object_or_404(TblJournalEntry, id=journal_id)

        # Get related credit and debit entries
        credit_entries = TblCrJournalEntry.objects.filter(journal_entry=journal_entry)
        debit_entries = TblDrJournalEntry.objects.filter(journal_entry=journal_entry)

        # Reverse the ledger operations for credit entries
        for credit_entry in credit_entries:
            ledger = credit_entry.ledger
            ledger_type = ledger.account_chart.account_type

            # Reverse the operation based on ledger type
            if ledger_type in ['Asset', 'Expense']:
                ledger.total_value += credit_entry.credit_amount
            elif ledger_type in ['Liability', 'Revenue', 'Equity']:
                ledger.total_value -= credit_entry.credit_amount

            ledger.save()
            # update_cumulative_ledger_bill(ledger)

        # Reverse the ledger operations for debit entries
        for debit_entry in debit_entries:
            ledger = debit_entry.ledger
            ledger_type = ledger.account_chart.account_type

            # Reverse the operation based on ledger type
            if ledger_type in ['Asset', 'Expense']:
                ledger.total_value -= debit_entry.debit_amount
            elif ledger_type in ['Liability', 'Revenue', 'Equity']:
                ledger.total_value += debit_entry.debit_amount

            ledger.save()
            # update_cumulative_ledger_bill(ledger)
        adjust_cumulative_ledger_afterentries(journal_entry)
 
        journal_entry.delete()


    except TblJournalEntry.DoesNotExist:
        # Handle the case where the journal entry doesn't exist.
        print("Journal Entry not found.")
    except Exception as e:
        # Handle any other exceptions or errors as needed
        print(f"An error occurred: {str(e)}")

class DeletePurchaseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        grn = data["grn"]

        try:
            purchase_obj = Purchase.objects.get(grn=int(grn))

        except Purchase.DoesNotExist:
            print(f"Purchase for {grn} did not exist")

        try:
            journal_entry = TblJournalEntry.objects.get(purchase=purchase_obj.id)
        except TblJournalEntry.DoesNotExist:
            print(f"Journal Entry did not exists for {purchase_obj.id}")

        delete_journal(journal_entry.id)


        ProductPurchase.objects.filter(purchase=purchase_obj).delete()
        purchase_obj.delete()
        try:
            purchase_entry_obj = TblpurchaseEntry.objects.get(grn=int(grn))
        except TblpurchaseEntry.DoesNotExist:
            print(f"Purchase for {grn} did not exist")
        purchase_entry_obj.delete()


        return Response("Purchase deleted successfully", 200)
          

from purchase.models import TblpurchaseReturn
class InsertPurchaseDetails(APIView):
    def get(self, request, *args, **kwargs):

        
        purchases = Purchase.objects.filter(status=True)

        for purchase in purchases:

            vendor_name = purchase.vendor
            bill_date = purchase.bill_date
            bill_no = purchase.bill_no
            total_quantity = 0
            vendor_pan = purchase.vendor.pan_no
            grand_total = purchase.grand_total
            non_taxable_amount = purchase.non_taxable_amount
            tax_amount = purchase.tax_amount
            purchase_id= purchase.id
            item_name = ''
            pp_no = ''

          
            TblpurchaseEntry.objects.create(
                bill_no=bill_no, bill_date=bill_date, pp_no=pp_no, vendor_name=vendor_name, vendor_pan=vendor_pan,
                item_name=item_name, quantity=total_quantity, amount=grand_total, tax_amount=tax_amount, non_tax_purchase=non_taxable_amount, purchase_id=purchase_id
            )

        void_purchases = Purchase.objects.filter(status=False)

        for purchase in void_purchases:

            vendor_name = purchase.vendor
            bill_date = purchase.bill_date
            bill_no = purchase.bill_no
            total_quantity = 0
            vendor_pan = purchase.vendor.pan_no
            grand_total = purchase.grand_total
            non_taxable_amount = purchase.non_taxable_amount
            tax_amount = purchase.tax_amount
            purchase_id= purchase.id
            item_name = ''
            pp_no = ''

          
            TblpurchaseReturn.objects.create(
                bill_no=bill_no, bill_date=bill_date, pp_no=pp_no, vendor_name=vendor_name, vendor_pan=vendor_pan,
                item_name=item_name, quantity=total_quantity, amount=grand_total, tax_amount=tax_amount, non_tax_purchase=non_taxable_amount
            )


        return Response({"detail": "Purchases has been inserted successfully"}, 200)

    
   


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
import decimal
from product.models import (
    Product
)
from purchase.models import  Purchase, Vendor ,ProductPurchase, TblpurchaseEntry
from accounting.models import AccountLedger,AccountSubLedger, AccountSubLedgerTracking, TblJournalEntry,TblDrJournalEntry, TblCrJournalEntry
from bill.utils import update_cumulative_ledger_bill, create_cumulative_ledger_bill
from accounting.utils import change_date_to_datetime

class ProductPurchaseAPI(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data

        try:
            # Basic purchase info
            purchase = Purchase.objects.create(
                bill_no=data["bill_no"],
                vendor_id=data["vendor_id"],
                sub_total=data["sub_total"],
                bill_date=data["bill_date"],
                discount_percentage=data.get("discount_percentage", 0),
                discount_amount=data.get("discount_amount", 0),
                taxable_amount=data.get("taxable_amount", 0),
                non_taxable_amount=data["non_taxable_amount"],
                tax_amount=data["tax_amount"],
                grand_total=data["grand_total"],
                amount_in_words=data.get("amount_in_words", ""),
                payment_mode=data["payment_mode"]
            )

            ledger_totals = {}
            total_quantity = 0

            for item in data["items"]:
                product = get_object_or_404(Product, pk=item["product_id"])
                ledger = get_object_or_404(AccountLedger, pk=item["ledger_id"])
                quantity = float(item["quantity"])
                rate = float(item["rate"])
                item_total = decimal.Decimal(quantity * rate)

                # Create subledger
                subledger_name = f'{product.title} ({product.category.title}) - Purchase'
                subledger, created = AccountSubLedger.objects.get_or_create(
                    sub_ledger_name=subledger_name,
                    ledger=ledger,
                    defaults={"total_value": 0}
                )
                prev_value = subledger.total_value
                subledger.total_value += item_total
                subledger.save()
                AccountSubLedgerTracking.objects.create(
                    subledger=subledger,
                    prev_amount=prev_value,
                    new_amount=subledger.total_value,
                    value_changed=subledger.total_value - prev_value
                )

                # Create ProductPurchase record
                ProductPurchase.objects.create(
                    product=product,
                    purchase=purchase,
                    quantity=quantity,
                    rate=rate,
                    item_total=item_total
                )

                ledger_totals[item["ledger_id"]] = ledger_totals.get(item["ledger_id"], 0) + item_total
                total_quantity += quantity

            # Save purchase entry for audit
            vendor = Vendor.objects.get(pk=data["vendor_id"])
            TblpurchaseEntry.objects.create(
                bill_no=data["bill_no"],
                bill_date=data["bill_date"],
                pp_no=data.get("pp_no", ""),
                vendor_name=vendor.name,
                vendor_pan=vendor.pan_no,
                item_name="",
                quantity=total_quantity,
                amount=data["grand_total"],
                tax_amount=data["tax_amount"],
                non_tax_purchase=data["non_taxable_amount"],
                purchase_id=purchase.id
            )

            # Create journal entry
            self.create_journal_entry(
                ledger_totals=ledger_totals,
                payment_mode=data["payment_mode"],
                username=request.user.username,
                tax_amount=decimal.Decimal(data["tax_amount"]),
                vendor_name=vendor.name,
                vendor_id=vendor.id,
                entry_date=data["bill_date"]
            )

            return Response({"message": "Purchase created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create_journal_entry(self, ledger_totals, payment_mode, username, tax_amount, vendor_name, vendor_id, entry_date):
        total_amount = sum(decimal.Decimal(amount) for amount in ledger_totals.values()) + tax_amount
        cash_ledger = get_object_or_404(AccountLedger, ledger_name='Cash-In-Hand')
        vat_receivable = get_object_or_404(AccountLedger, ledger_name='VAT Receivable')

        journal = TblJournalEntry.objects.create(
            employee_name=username,
            journal_total=total_amount,
            entry_date=entry_date
        )
        entry_datetime = change_date_to_datetime(entry_date)

        for ledger_id, amount in ledger_totals.items():
            ledger = get_object_or_404(AccountLedger, pk=int(ledger_id))
            TblDrJournalEntry.objects.create(
                journal_entry=journal,
                particulars=f"Automatic: {ledger.ledger_name} A/c Dr.",
                debit_amount=amount,
                ledger=ledger
            )
            ledger.total_value += amount
            ledger.save()
            update_cumulative_ledger_bill(ledger, entry_datetime)

        if tax_amount > 0:
            TblDrJournalEntry.objects.create(
                journal_entry=journal,
                particulars="Automatic: VAT Receivable A/c Dr.",
                debit_amount=tax_amount,
                ledger=vat_receivable
            )
            vat_receivable.total_value += tax_amount
            vat_receivable.save()
            update_cumulative_ledger_bill(vat_receivable, entry_datetime)

        # Credit side based on payment mode
        credit_particulars = f"Automatic: To "
        if payment_mode.lower() == "credit":
            try:
                vendor_ledger = AccountLedger.objects.get(ledger_name=str(vendor_id) + vendor_name)
            except AccountLedger.DoesNotExist:
                chart = AccountChart.objects.get(group__iexact='Sundry Creditors')
                vendor_ledger = AccountLedger.objects.create(
                    ledger_name=str(vendor_id) + ' ' + vendor_name,
                    total_value=0,
                    is_editable=True,
                    account_chart=chart
                )
                create_cumulative_ledger_bill(vendor_ledger, entry_datetime)
            vendor_ledger.total_value += total_amount
            vendor_ledger.save()
            update_cumulative_ledger_bill(vendor_ledger, entry_datetime)
            ledger = vendor_ledger
        elif payment_mode.lower() == "mobile payment":
            ledger = get_object_or_404(AccountLedger, ledger_name='Mobile Payments')
            ledger.total_value -= total_amount
        elif payment_mode.lower() == "credit card":
            ledger = get_object_or_404(AccountLedger, ledger_name='Card Transactions')
            ledger.total_value -= total_amount
        elif payment_mode.lower() == "complimentary":
            ledger = get_object_or_404(AccountLedger, ledger_name='Complimentary Expenses')
            ledger.total_value -= total_amount
        else:
            ledger = cash_ledger
            ledger.total_value -= total_amount

        ledger.save()
        update_cumulative_ledger_bill(ledger, entry_datetime)

        TblCrJournalEntry.objects.create(
            journal_entry=journal,
            particulars=f"{credit_particulars}{ledger.ledger_name} A/c",
            credit_amount=total_amount,
            ledger=ledger
        )
