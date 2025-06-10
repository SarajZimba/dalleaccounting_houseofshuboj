from django.urls import path
from api.views.credit_journal_entry import CreditJournalEntryAPIView

urlpatterns = [
    # Your other URL patterns
    path('create_credit_journal_entry/', CreditJournalEntryAPIView.as_view(), name='create_credit_journal_entry_api'),
]