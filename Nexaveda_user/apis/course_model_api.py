"""Course APIs to manage CRUD operations."""

from rest_framework.views import APIView
from Nexaveda_user.serializers.course_creation_serializer import CourseSerializer
from rest_framework.response import Response
from rest_framework import status
from Nexaveda_user.models.courses_model import CoursesModel
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class CourseAPI(APIView):
    """
    API to list all active courses or add a new course.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch all active courses."""
        courses = CoursesModel.objects.filter(is_active=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(
            {"message": "Courses fetched successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Create a new course."""
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Course added successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )


class CourseDetailAPI(APIView):
    """
    API to update or soft delete a particular course.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        """Update course partially."""
        course = get_object_or_404(CoursesModel, id=id, is_active=True)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Course updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request, id):
        """Soft delete a course."""
        course = get_object_or_404(CoursesModel, id=id, is_active=True)
        course.is_active = False
        course.save()
        return Response(
            {"message": "Course deleted (soft delete)"},
            status=status.HTTP_200_OK
        )
