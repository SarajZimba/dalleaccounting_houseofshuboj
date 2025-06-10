from rest_framework.routers import DefaultRouter
from api.views.student_attendancecanteen import PreInformedLeaveViewSet

router = DefaultRouter()
router.register(r'preinformed-leave', PreInformedLeaveViewSet, basename='preinformed-leave')

urlpatterns = router.urls