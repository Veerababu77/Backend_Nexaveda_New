
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Nexaveda_user.serializers.course_creation_serializer import RatingSerializer
from Nexaveda_user.models.courses_model import CoursesModel

class RatingAPI(APIView):
    
    def post(self, request, course_id):
        course = get_object_or_404(CoursesModel, id = course_id)
        serializer = RatingSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(course = course)
        return Response({"message":"Rating is added to the Course"}, status = status.HTTP_200_OK)
        