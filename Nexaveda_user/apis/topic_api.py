
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Nexaveda_user.models.courses_model import TopicModel
from Nexaveda_user.serializers.topic_serializer import TopicSerializerIndividual

class TopicAPI(APIView):
    def patch(self, request, id):
        try:
            topic = TopicModel.objects.get(id = id)
        except TopicModel.DoesNotExist:
            return Response({"message":"Topic with this id is not exsits"}, status = status.HTTP_404_NOT_FOUND)
        serializer = TopicSerializerIndividual(topic, data = request.data, partial = True)
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
    