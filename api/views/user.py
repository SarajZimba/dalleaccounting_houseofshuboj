from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from user.models import Customer
from ..serializers.user import CustomTokenPairSerializer, CustomerSerializer

from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer


class CustomerAPI(ModelViewSet):
    serializer_class = CustomerSerializer
    model = Customer
    queryset = Customer.objects.active()
    pagination_class = None

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user import AgentSerializer
from django.contrib.auth.models import Group


class AgentViewSet(viewsets.ViewSet):
    serializer_class = AgentSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            usercode = serializer.validated_data['username']
            full_name = serializer.validated_data['full_name']

            user = User.objects.create(username=usercode, full_name=full_name, is_superuser=False, is_staff=True)

            user.set_password(usercode)
            user.save()

            group = Group.objects.get(name="agent")
            user.groups.add(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
        
            return Response({"detail":"User with the username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
from rest_framework.views import APIView  
class PostCustomerListAPI(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data

        serializer = CustomerSerializer(data=data, many=True)
        
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"data":"Customers created successfully"}, 200)
            else:
                return Response({"data": "The given data was not valid"}, 400)
        except Exception as e:
            print(str(e))
            return Response({"error": "Data was not valid" + str(e)}, 400)
            
from bill.models import Bill
from rest_framework.views import APIView  
class DeleteCustomerAPI(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data
        
        customer_id = data.get("customer_id", None)

        if customer_id is None:
            return Response({"error":"Please provide customer id"}, 400)
        
        customer_obj = Customer.objects.filter(id=int(customer_id)).first()

        if customer_obj is None:
            return Response({"error":"No customer found of that id"}, 400)
        
        customer_bills = Bill.objects.filter(customer = customer_obj).exists()

        if customer_bills:
            customer_obj.status=False
            customer_obj.is_deleted  =True
            customer_obj.save()
            return Response({"message":"This customer already has bills on his name . We cannot delete it but can be changed to inactive", "flag":False}, 200)
        
        if not customer_bills:
            customer_obj.delete()
            return Response("Customer has been deleted successfully", 200)
            
class UpdateCustomerStudentClass(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        old_class = data.get("old_class", None)
        new_class = data.get("new_class", None)

        if old_class is None:
            return Response("Provide old_class", 400)
        if new_class is None:
            return Response("Provide new_class", 400)
        students = Customer.objects.filter(student_class__isnull=False)

        try:
            # Use bulk update with `update()` method
            students.filter(student_class=old_class).update(student_class=new_class)
            return Response(f" student classes updated.", 200)
        except Exception as e:
            return Response({"error" : str(e)}, 400)

class StatusToggleStudent(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        student_id = data.get("student_id", None)

        if student_id is None:
            student = Customer.objects.get(id=int(student_id))
            student.status = False
            student.is_deleted = True
            student.save()
            return Response(f"Student has been deleted successfully", 200)            

        else:
            return Response({"error" : "Student not found"}, 400)
            
from api.serializers.user import StudentSerializer
class StudentsAPI(APIView):

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.filter(student_class__isnull=False, roll_no__isnull=False, section__isnull=False, status=True, is_deleted=False)

        serializer = StudentSerializer(customers, many=True)

        return Response(serializer.data, 200)