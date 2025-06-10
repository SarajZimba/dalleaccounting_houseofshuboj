# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from user.models import Customer
from api.serializers.section import SectionSerializer

class CustomerSectionList(APIView):
    def get(self, request, *args, **kwargs):
        student_class = request.query_params.get('student_class', None)
        
        if not student_class:
            return Response(
                {"error": "student_class parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            student_class = int(student_class)
        except ValueError:
            return Response(
                {"error": "student_class must be a valid integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sections = Customer.objects.filter(
            student_class=student_class,
            section__isnull=False
        ).exclude(section__exact='').values('section').annotate(
            count=Count('section')
        ).order_by('section')
        
        serializer = SectionSerializer([{'section': item['section']} for item in sections], many=True)
        
        return Response(serializer.data)