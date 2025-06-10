from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.commision import tblEmployeeCommisionSerializer



class CreatetblEmpoyeeCommisionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = request.data 

        serializer = tblEmployeeCommisionSerializer(data=posted_data, many=True)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Commision saved successfully"}, 200)
        except Exception as e:
            return Response({"detail": serializer.errors}, status=400)  # Return validation errors