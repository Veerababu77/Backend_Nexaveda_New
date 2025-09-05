from rest_framework import serializers
from Nexaveda_user.models.courses_model import CoursesModel, TopicModel, SubtopicModel

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtopicModel
        fields = ["id", "subtopic", "topic", "created_at"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicModel
        fields = ["id", "title", "created_at"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesModel
        fields = [
            "id", "course_name", "description", "duration_in_days",
            "course_level", "course_cost", "course_discount",
            "is_active", "created_at", "instructor"
        ]
