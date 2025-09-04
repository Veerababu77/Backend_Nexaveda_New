
from rest_framework.views import APIView
from Nexaveda_user.serializers.course_creation_serializer import CourseCreationSerializer
from rest_framework.response import Response
from rest_framework import status
from Nexaveda_user.models.courses_model import CoursesModel

class CourseAPI(APIView):
    
    def get(self,request):
        course_snippet = CoursesModel.objects.filter(is_active = True)
        serializer = CourseCreationSerializer(course_snippet, many = True)
        return Response({"message":"Courses fetched successfully", "data" : serializer.data}, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CourseCreationSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"message":"Course added to Course Model"}, status = status.HTTP_200_OK)