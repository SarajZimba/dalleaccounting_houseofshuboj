from django.urls import path
from api.views.journal_entry import JournalEntryAPIView

urlpatterns = [
    # Your other URL patterns
    path('create_journal_entry/', JournalEntryAPIView.as_view(), name='create_journal_entry_api'),
]