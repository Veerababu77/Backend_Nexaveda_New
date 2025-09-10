
from rest_framework.views import APIView
from Nexaveda_user.serializers.attendence_serializer import AttendenceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class AttendenceAPI(APIView):
    
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AttendenceSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                "message" : "Attendence marked.",
                "data" : serializer.data
            }, status = status.HTTP_200_OK
        )
        