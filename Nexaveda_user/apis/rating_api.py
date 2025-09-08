
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Nexaveda_user.serializers.course_creation_serializer import RatingSerializer
from Nexaveda_user.models.courses_model import CoursesModel, RatingModel
from rest_framework.permissions import IsAuthenticated

class RatingAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id):
        user = request.user
        course = get_object_or_404(CoursesModel, id = course_id)
        rating_value = request.data.get("rating", 5)
        rating,created = RatingModel.objects.update_or_create(
            user = user,
            course = course,
            defaults={"rating": rating_value},
        )
        serializer = RatingSerializer(rating)
        return Response({"message": "Rating created" if created else "Rating updated"}, status = status.HTTP_200_OK)
        