
from rest_framework import serializers
from django.db.models import Avg
from Nexaveda_user.models.courses_model import CoursesModel, TopicModel, SubtopicModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtopicModel
        fields = ["subtopic"]

class TopicSerializer(serializers.ModelSerializer):
    subtopic = SubtopicSerializer(many = True)
    class Meta:
        model = TopicModel
        fields = ["title", "subtopic"]
        
class CourseCreationSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many = True)
    avg_rating = serializers.SerializerMethodField()
    instructor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    actual_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CoursesModel
        fields = ["course_name","description","duration_in_days","course_level","course_cost","actual_price","is_active","topics", "avg_rating", "instructor"]
        
    def validate_course_name(self, value):
        if CoursesModel.objects.filter(course_name__iexact = value).exists():
            raise ValidationError({"message": "Course with this course name is already exists."})
        return value
    def get_actual_price(self, obj):
        if obj.course_discount:
            return round(obj.course_cost * 100 / (100 - obj.course_discount), 2)
        return obj.course_cost

    def get_avg_rating(self, obj):
        return obj.courses.aggregate(Avg("rating"))['rating__avg'] or 0
    
    def get_instructor(self,obj):
        return obj.instructor.username if obj.instructor else None
    
    def create(self, validated_data):
        topics_data = validated_data.pop("topics", [])
        course = CoursesModel.objects.create(**validated_data)
        
        for topic_data in topics_data:
            subtopic_data = topic_data.pop("subtopic", [])
            topic = TopicModel.objects.create(course = course, **topic_data)
            
            for sub_topic_data in subtopic_data:
                SubtopicModel.objects.create(topics = topic, **sub_topic_data)
        return course
    
    
    