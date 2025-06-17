from django.shortcuts import render
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from root.utils import DeleteMixin
from .models import StudentAttendance
from .forms import StudentAttendanceForm

from user.permission import IsAdminMixin

class StudentCanteenAttendanceMixin(IsAdminMixin):
    model = StudentAttendance
    form_class = StudentAttendanceForm
    paginate_by = 50
    queryset = StudentAttendance.objects.filter(status=True, is_deleted=False)
    success_url = reverse_lazy("studentcanteenattendance_list")
    search_lookup_fields = [
        "title",
        "description",
    ]

from django.db.models import Count, Sum
from django.shortcuts import render
from .models import StudentAttendance
from product.models import Product
class StudentCanteenAttendanceList(StudentCanteenAttendanceMixin, ListView):
    template_name = "studentcanteenattendance/studentcanteenattendance_list.html"

    def get_queryset(self):
        # Start with the base query
        queryset = (
            StudentAttendance.objects
            .filter(status=True, is_deleted=False, bill_created=False)
            .values('student', 'student__name', 'student__student_class', 'student__roll_no', 'student__section')
            .annotate(no_of_entries=Count('id'), total_sum=Sum('total'))
            .order_by('-no_of_entries')
        )
        
        # If a class is provided in the GET parameters, filter by student class
        student_class = self.request.GET.get('student_class')
        if student_class:
            queryset = queryset.filter(student__student_class=student_class)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the meal entries
        meal_eatens_by_students = list(self.get_queryset())

        distinct_classes = Customer.objects.filter(
            status=True,
            is_deleted=False,
            student_class__isnull=False
        ).order_by('student_class') \
        .values('student_class') \
        .distinct()

        distinct_classes = sorted(
            [{'student__student_class': item['student_class']} for item in distinct_classes],
            key=lambda x: int(x['student__student_class'])
        )
        context['distinct_classes'] = distinct_classes
        context['meal_eatens_by_students'] = meal_eatens_by_students
        return context

class StudentCanteenAttendanceDetail(StudentCanteenAttendanceMixin, DetailView):
    template_name = "studentcanteenattendance/studentcanteenattendance_detail.html"


class StudentCanteenAttendanceCreate(StudentCanteenAttendanceMixin, CreateView):
    template_name = "create.html"


class StudentCanteenAttendanceUpdate(StudentCanteenAttendanceMixin, UpdateView):
    pass



class StudentCanteenAttendanceDelete(StudentCanteenAttendanceMixin, DeleteMixin, View):
    pass


from django.shortcuts import render
from bill.models import Bill

from urllib.parse import unquote

from django.utils import timezone
from urllib.parse import unquote, parse_qs
from django.http import QueryDict

def print_multiple_bills(request, pk):
    # Decode the URL-encoded class name
    student_class = unquote(pk)
    
    # Get month and year from query parameters
    month = request.GET.get('month')  # None is default
    year = request.GET.get('year')    # None is default
    
    # If month/year not provided, use current month/year
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    # Query bills for this class
    bills = Bill.objects.filter(customer__student_class=student_class)
    
    # Apply month/year filters if provided, otherwise use current month/year
    if month and year:
        bills = bills.filter(month=month, year=year)
    else:
        bills = bills.filter(month=current_month, year=current_year)
    
    # Calculate totals
    for bill in bills:
        bill.total_quantity = sum(item.product_quantity for item in bill.bill_items.all())
        bill.total_amount = sum(item.amount for item in bill.bill_items.all())
    
    return render(request, 'bill/studentbilldetail.html', {
        'bills': bills,
        'class_name': student_class,
        'selected_month': month or current_month,  # Show selected or current
        'selected_year': year or current_year      # Show selected or current
    })

from django.db.models import Count, Q
from user.models import Customer
from django.http import JsonResponse

from django.db.models import Q
import datetime
from django.utils import timezone
from canteen.models import MonthlyAdjustments

def bill_details_view(request):
    # Get filter parameters
    student_class = request.GET.get('student_class')
    student_section = request.GET.get('student_section')
    student_name = request.GET.get('student_name')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    
    # Prepare month choices (1-12 with names)
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    # Prepare year choices (current year and some past/future years)
    years = range(current_year - 2, current_year + 3)
    
    
    distinct_classes = Customer.objects.filter(
        status=True, 
        is_deleted=False, 
        student_class__isnull=False
    ).values('student_class').distinct()

    # Convert to list and remove duplicates
    distinct_classes = [{'student_class': item['student_class']} for item in distinct_classes]
    distinct_classes = [dict(t) for t in {tuple(d.items()) for d in distinct_classes}]

    # Sort numerically if possible
    try:
        distinct_classes.sort(key=lambda x: int(x['student_class']))
    except (ValueError, TypeError):
        distinct_classes.sort(key=lambda x: x['student_class'])
    
    # Initialize bills as empty queryset
    bills = Bill.objects.none()
    
    # Build filter conditions
    filters = Q()
    print('student section from get', student_section)
    if student_class:
        filters &= Q(customer__student_class=student_class)
    if student_section is not None and student_section != '':
        filters &= Q(customer__section=student_section)
    if student_name:
        filters &= Q(customer__name__icontains=student_name)
    
    # Date filtering
    date_filters = Q()
    if year_filter:
        date_filters &= Q(year=year_filter)
    if month_filter:
        date_filters &= Q(month=month_filter)
    
    # Only query bills if at least one filter is provided
    if student_class or student_section or student_name or month_filter or year_filter:
        bills = Bill.objects.filter(filters & date_filters)
        
        # Calculate totals
        for bill in bills:
            bill.total_quantity = sum(item.product_quantity for item in bill.bill_items.all())
            bill.total_amount = sum(item.amount for item in bill.bill_items.all())
            # Get monthly adjustments for this bill's month/year
            if bill.month and bill.year and bill.customer:
                # Get all unprocessed holidays that affected this bill
                unprocessed_holidays = MonthlyAdjustments.objects.filter(
                    Q(valid_for_month=bill.month, valid_for_year=bill.year, considered_next_month=True)
                ).distinct()
                
                # Prepare product references for this student
                student = bill.customer
                veg_product = Product.objects.filter(
                    is_canteen_item=True, lunch_type="veg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
                egg_product = Product.objects.filter(
                    is_canteen_item=True, lunch_type="egg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
                nonveg_product = Product.objects.filter(
                    is_canteen_item=True, lunch_type="nonveg",
                    min_class__lte=student.student_class,
                    max_class__gte=student.student_class
                ).first()
                
                # Calculate adjusted products for each holiday
                adjusted_products = []
                for holiday in unprocessed_holidays:
                    holiday_date = holiday.holiday_date
                    day_name = holiday_date.strftime("%A")
                    preference = student.meal_preference
                    
                    product_to_subtract = None
                    
                    if day_name == "Wednesday":
                        if preference == "nonveg" and nonveg_product:
                            product_to_subtract = nonveg_product
                        else:
                            product_to_subtract = veg_product
                    elif day_name == "Friday":
                        if preference in ["egg", "nonveg"] and egg_product:
                            product_to_subtract = egg_product
                        else:
                            product_to_subtract = veg_product
                    else:
                        product_to_subtract = veg_product
                    
                    if product_to_subtract:
                        adjusted_products.append({
                            'product': product_to_subtract,
                            'holiday_date': holiday_date,
                            'reason': f"Holiday on {holiday_date.strftime('%Y-%m-%d')}"
                        })
                
                bill.adjusted_products = adjusted_products
            else:
                bill.adjusted_products = []
    
    # Get sections for the selected class (if any)
    sections_for_class = []
    if student_class:
        sections_for_class = Customer.objects.filter(
            student_class=student_class,
            section__isnull=False
        ).exclude(section__exact='').values_list('section', flat=True).distinct()
    
    # For AJAX requests (section dropdown)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'sections': list(sections_for_class),
            'current_section': request.GET.get('student_section', '')
        })
    
    return render(request, 'bill/studentbilldetail.html', {
        'bills': bills,
        'distinct_classes': distinct_classes,
        'sections_for_class': sections_for_class,
        'months': months,
        'years': years,
        'current_month': current_month,
        'current_year': current_year,
    })


import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone
from rest_framework_simplejwt.tokens import AccessToken
@login_required
def generate_login_token_and_redirect(request):
    token = AccessToken.for_user(request.user)
    # Optional: set custom expiry time (e.g., 5 minutes)
    token.set_exp(from_time=datetime.now(timezone.utc) + timedelta(minutes=5))

    react_login_url = f"https://attendance.houseofshuboja.silverlinepos.com/auth?token={str(token)}"
    return redirect(react_login_url)

def single_bill_detail_view(request, pk):
    # Query to get all bills you want to display, e.g., all bills from a certain date or status
    bill = Bill.objects.get(id=pk)
    # Get distinct student classes and add to context

    return render(request, 'bill/single_studentbilldetail.html', {'bill': bill})

