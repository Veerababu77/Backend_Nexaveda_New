
from rest_framework.views import APIView
from Nexaveda_user.serializers.course_creation_serializer import CourseSerializer
from rest_framework.response import Response
from rest_framework import status
from Nexaveda_user.models.courses_model import CoursesModel
from rest_framework.permissions import IsAuthenticated

class CourseAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self,request):
        course_snippet = CoursesModel.objects.filter(is_active = True)
        serializer = CourseSerializer(course_snippet, many = True)
        return Response({"message":"Courses fetched successfully", "data" : serializer.data}, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CourseSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"message":"Course added to Course Model"}, status = status.HTTP_200_OK)
    
class CourseDetailAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        course = CoursesModel.objects.get(id = id)
        serializer = CourseSerializer(course, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"message":"Course updated sucessfully"}, status = status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            course = CoursesModel.objects.get(id = id)
            course.delete()
            return Response({"message": "Course deleted succesfully"}, status = status.HTTP_204_NO_CONTENT)
        except CoursesModel.DoesNotExist:
            return Response({"message":"Course with this id is not found"}, status = status.HTTP_404_NOT_FOUND)