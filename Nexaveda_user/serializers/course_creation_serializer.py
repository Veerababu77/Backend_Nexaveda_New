from rest_framework import serializers
from django.db.models import Avg
from Nexaveda_user.models.courses_model import CoursesModel, TopicModel, SubtopicModel, RatingModel

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingModel
        fields = ["id", "rating"]

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtopicModel
        fields = ["id", "subtopic", "created_at"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicModel
        fields = ["id", "title", "created_at"]


class CourseSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = CoursesModel
        fields = [
            "id", "course_name", "description", "duration_in_days",
            "course_level", "course_cost", "course_discount",
            "is_active", "created_at", "instructor","avg_rating","course_pic"
        ]
    def get_avg_rating(self,obj):
        return obj.courses.aggregate(avg = Avg("rating"))["avg"] or 0

class TopicGetSerializer(serializers.ModelSerializer):
    subtopic = SubtopicSerializer(read_only = True, many = True)
    class Meta:
        model = TopicModel
        fields = ["id", "title", "created_at", "subtopic"]
class CourseGetSerializer(serializers.ModelSerializer):
    topics = TopicGetSerializer(many = True)
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = CoursesModel
        fields = [
            "id", "course_name", "description", "duration_in_days",
            "course_level", "course_cost", "course_discount",
            "is_active", "created_at", "instructor","avg_rating", "topics"
        ]
        
    def get_avg_rating(self,obj):
        return obj.courses.aggregate(avg = Avg("rating"))["avg"] or 0

