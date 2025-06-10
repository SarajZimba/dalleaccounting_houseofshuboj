from api.views.studentbillhistory import StudentHistory, StudentBillPreview, StudentHistoryCanteen # Import your view
from django.urls import path

urlpatterns = [
    # Other URL patterns...
    path('studenthistory-report/', StudentHistory.as_view(), name='studenthistory-report'),
    path('studentbill-preview/', StudentBillPreview.as_view(), name='studentbill-preview'),
    path('studenthistory-canteen/', StudentHistoryCanteen.as_view(), name='studenthistory-canteen'),
]