
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Nexaveda_user.models.courses_model import TopicModel, CoursesModel
from Nexaveda_user.serializers.course_creation_serializer import TopicSerializer

class TopicAPI(APIView):
    def post(self, request, course_id):
        try:
            course = CoursesModel.objects.get(id = course_id)
        except CoursesModel.DoesNotExist:
            return Response({"message":"Course is not exists"}, status = status.HTTP_400_BAD_REQUEST)
        serializer = TopicSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(course = course)
        return Response({"message":"Topic created successfully", "data" : serializer.data}, status = status.HTTP_200_OK)

class TopicDetailAPI(APIView):
    def patch(self, request, id):
        try:
            topic = TopicModel.objects.get(id = id)
        except TopicModel.DoesNotExist:
            return Response({"message":"Topic with this id is not exsits"}, status = status.HTTP_404_NOT_FOUND)
        serializer = TopicSerializer(topic, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"message":"Topic saved successfully"}, status = status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            course = TopicModel.objects.get(id = id)
            course.delete()
            return Response({"message": "Topic deleted succesfully"}, status = status.HTTP_204_NO_CONTENT)
        except TopicModel.DoesNotExist:
            return Response({"message":"Topic with this id is not found"}, status = status.HTTP_404_NOT_FOUND)
    