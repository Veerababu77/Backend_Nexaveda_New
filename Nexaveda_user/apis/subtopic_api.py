
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from Nexaveda_user.models.courses_model import TopicModel, SubtopicModel
from Nexaveda_user.serializers.course_creation_serializer import SubtopicSerializer
from rest_framework.permissions import IsAuthenticated

class SubtopicAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, topic_id):
        try:
            topic = TopicModel.objects.get(id = topic_id)
        except TopicModel.DoesNotExist:
            return Response({"message":"Topic with this id is not exists"}, status = status.HTTP_400_BAD_REQUEST)
        serializer = SubtopicSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(topics = topic)
        return Response({
            "message":"Subtopic added to topic successfully",
            "data" : serializer.data
        }, status = status.HTTP_200_OK)

class SubtopicDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        try:
            subtopic = SubtopicModel.objects.get(id = id)
        except SubtopicModel.DoesNotExist:
            return Response({"message":"Subtopic doesn't exists with this id"}, status = status.HTTP_400_BAD_REQUEST)
        serializer = SubtopicSerializer(subtopic, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({
            "message":"Sub topic updated successfully",
            "data" : serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        subtopic = get_object_or_404(SubtopicModel, id = id)
        subtopic.delete()
        return Response({"message":"Sub topic deleted successfully"}, status=status.HTTP_200_OK)