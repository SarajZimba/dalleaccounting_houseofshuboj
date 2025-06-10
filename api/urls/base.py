from .user import urlpatterns as user_urlpatterns
from .product import urlpatterns as product_urlpatterns
from .bill import urlpatterns as bill_urlpatterns
from .organization import urlpatterns as org_urlpatterns
from .discount_urls import urlpatterns as discount_urlspatterns
from .purchaserequisition_api import urlpatterns as purchaserequisition_urlpattern
from .accounting_urls import urlpatterns as accounting_urlpatterns
from .mobilepayment_type import urlpatterns as mobile_urlpatterns
from .endday_report import urlpatterns as enddayreport_urlpatterns
from .today_report import urlpatterns as todayreport_urlpatterns
from .category_wise_report import urlpatterns as category_wise_sale_urlpatterns
from .report import urlpatterns as report_urlpatterns 
from.master import urlpatterns as master_urlpatterns
from .bill_todayid import urlpatterns as bill_todayid_urlpatterns
from .journal_entry import urlpatterns as journal_entry_urls
from .credit_journal_entry import urlpatterns as credit_journal_entry_urls
from .give_ledger import urlpatterns as give_ledger_urls
from .vendor import urlpatterns as vendor_urlpatterns
from .employee import urlpatterns as employee_urlpatterns
from .paid_leaves import urlpatterns as paid_leaves_urlpatterns
from .salary_sheet import urlpatterns as salary_sheet_urlptterns
from .deduction import urlpatterns as deduction_urlptterns
from .commision import urlpatterns as commision_urlpatterns
from .purchase import urlpatterns as purchase_urlpatterns
from .canteen import urlpatterns as canteen_urlpatterns
from .working_days import urlpatterns as working_days_urlpatterns
from .holiday import urlpatterns as holiday_urlpatterns
from .student_attendancecanteen import urlpatterns as student_canteenattendance_urlpatterns
from .section import urlpatterns as section_urlpatterns
# from .schoolcanteen_credit import urlpatterns as schoolcanteen_urlpatterns
from .monthlyadjustments import urlpatterns as monthlyadjustment_urlpatterns
from .studentbillhistory import urlpatterns as studentbillhistory_urlpatterns

urlpatterns = (
    [] + user_urlpatterns + product_urlpatterns + bill_urlpatterns + org_urlpatterns+discount_urlspatterns+purchaserequisition_urlpattern+accounting_urlpatterns+mobile_urlpatterns+enddayreport_urlpatterns+todayreport_urlpatterns+category_wise_sale_urlpatterns +report_urlpatterns+ master_urlpatterns+ bill_todayid_urlpatterns+ journal_entry_urls  + credit_journal_entry_urls + give_ledger_urls + vendor_urlpatterns + employee_urlpatterns + paid_leaves_urlpatterns + salary_sheet_urlptterns+ deduction_urlptterns+ commision_urlpatterns+ purchase_urlpatterns + canteen_urlpatterns + working_days_urlpatterns + holiday_urlpatterns + student_canteenattendance_urlpatterns + section_urlpatterns + monthlyadjustment_urlpatterns + studentbillhistory_urlpatterns
)
