from rest_framework import serializers
from Nexaveda_user.models.courses_model import TopicModel
from rest_framework.exceptions import ValidationError

class TopicSerializerIndividual(serializers.ModelSerializer):
    
    class Meta:
        model = TopicModel
        fields = ["id","title"]
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance