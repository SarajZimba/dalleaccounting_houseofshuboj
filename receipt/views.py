from django.views.generic import ListView
from receipt.models import Receipt
from django.db.models import Q

class ReceiptListView(ListView):
    model = Receipt
    template_name = 'receipt/receipt_list.html'
    context_object_name = 'receipts'
    ordering = ['-transaction_date_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(Q(receipt_number__icontains=search_query))
        return queryset




from django.views.generic import DetailView
from receipt.models import Receipt
from organization.models import Organization

class ReceiptDetailView(DetailView):
    model = Receipt
    template_name = 'receipt/receipt_card.html'
    context_object_name = 'receipt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = Organization.objects.first()
        return context

