# views.py
from rest_framework import viewsets
from canteen.models import PreInformedLeave
from api.serializers.student_attendancecanteen import PreInformedLeaveSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class PreInformedLeaveViewSet(viewsets.ModelViewSet):
    queryset = PreInformedLeave.objects.all()
    serializer_class = PreInformedLeaveSerializer
    permission_classes = [AllowAny]
