
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Nexaveda_user.models.certificates_model import Certificates
from Nexaveda_user.serializers.certificates_serializer import CertificatesSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CertificatesAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        ceritificates = Certificates.objects.filter(user = user)
        serializer = CertificatesSerializer(ceritificates, many = True)
        return Response({"message":"certificates fetched successfully", "data":serializer.data}, status = status.HTTP_200_OK)
    
# class CertificatesPostAPI(APIView):
    
#     def post(self, request, users):
#         serializer = CertificatesSerializer()
#         pass
    

    