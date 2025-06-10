from django.db import models

from root.utils import BaseModel
from accounting.models import AccountLedger

import inflect
from django.db import models
from accounting.models import AccountLedger
from root.utils import BaseModel
from organization.models import Branch  # if you have a branch model

p = inflect.engine()

def amount_to_words_en(amount):
    rupees = int(amount)
    paise = round((amount - rupees) * 100)

    words = p.number_to_words(rupees) + " rupees"
    if paise > 0:
        words += " and " + p.number_to_words(paise) + " paisa"
    return words


# Create your models here.
class Receipt(BaseModel):
    fiscal_year = models.CharField(max_length=20)
    agent_name = models.CharField(max_length=255, null=True)
    # customer = models.ForeignKey("user.Customer", on_delete=models.SET_NULL, null=True)
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receipt_number = models.CharField(max_length=255, null=True, blank=True)
    amount_in_words = models.TextField(null=True, blank=True)
    payment_mode = models.CharField(
        max_length=255, default="Cash", blank=True, null=True
    )
    print_count = models.PositiveIntegerField(default=1)
    # is_taxable = models.BooleanField(default=True)
    receipt_count_number = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    received_from_ledger = models.ForeignKey(AccountLedger, models.CASCADE, null=True, blank=True, related_name='receipts_sent_from_customer')   
    received_to_ledger = models.ForeignKey(AccountLedger, models.CASCADE, null=True, blank=True, related_name='receipts_received_to_ledger')   

    class Meta:
        unique_together = 'receipt_number', 'fiscal_year'

    def __str__(self):
        return f"{self.transaction_date}- {self.grand_total}"

    def save(self, *args, **kwargs):
        # Set amount in words
        if self.grand_total:
            self.amount_in_words = amount_to_words_en(float(self.grand_total))

        # Set receipt_count_number only if it's not already set
        if not self.receipt_count_number:
            latest = Receipt.objects.filter(fiscal_year=self.fiscal_year).order_by('-receipt_count_number').first()
            self.receipt_count_number = (latest.receipt_count_number + 1) if latest and latest.receipt_count_number else 1
            new_count_number = self.receipt_count_number
        # Set receipt_number using branch code
        if not self.receipt_number:
            branch = Branch.objects.filter(is_central_billing=True).first()
            if branch:
                self.receipt_number = f"{branch.branch_code}-{new_count_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_date} - {self.grand_total}"