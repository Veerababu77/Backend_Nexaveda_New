from rest_framework import serializers
from django.db.models import Avg
from Nexaveda_user.models.courses_model import CoursesModel, TopicModel, SubtopicModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class SubtopicSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = SubtopicModel
        fields = ["id", "subtopic"]


class TopicSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    subtopic = SubtopicSerializer(many=True)

    class Meta:
        model = TopicModel
        fields = ["id", "title", "subtopic"]


class CourseSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()
    actual_price = serializers.SerializerMethodField()
    instructor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = CoursesModel
        fields = [
            "id", "course_name", "description", "duration_in_days", "course_level",
            "course_cost", "actual_price", "is_active", "topics", "avg_rating", "instructor"
        ]

    def validate_course_name(self, value):
        qs = CoursesModel.objects.filter(course_name__iexact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise ValidationError("Course with this name already exists.")
        return value

    def get_actual_price(self, obj):
        if obj.course_discount:
            return round(obj.course_cost * 100 / (100 - obj.course_discount), 2)
        return obj.course_cost

    def get_avg_rating(self, obj):
        return obj.courses.aggregate(Avg("rating"))['rating__avg'] or 0

    def create(self, validated_data):
        topics_data = validated_data.pop("topics", [])
        course = CoursesModel.objects.create(**validated_data)
        self._update_topics(course, topics_data)
        return course

    def update(self, instance, validated_data):
        topics_data = validated_data.pop("topics", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._update_topics(instance, topics_data)
        return instance

    def _update_topics(self, course_instance, topics_data):
        incoming_topic_ids = []

        for topic_data in topics_data:
            sub_topics_data = topic_data.pop("subtopic", [])
            topic_id = topic_data.pop("id", None)

            if topic_id:
                topic, _ = TopicModel.objects.update_or_create(
                    id=topic_id, course=course_instance, defaults=topic_data
                )
            else:
                topic = TopicModel.objects.create(course=course_instance, **topic_data)

            incoming_topic_ids.append(topic.id)

            incoming_subtopic_ids = []
            for subtopic_data in sub_topics_data:
                subtopic_id = subtopic_data.pop("id", None)
                if subtopic_id:
                    subtopic, _ = SubtopicModel.objects.update_or_create(
                        id=subtopic_id, topics=topic, defaults=subtopic_data
                    )
                else:
                    subtopic = SubtopicModel.objects.create(topics=topic, **subtopic_data)
                incoming_subtopic_ids.append(subtopic.id)

            # Delete subtopics not in payload
            SubtopicModel.objects.filter(topics=topic).exclude(id__in=incoming_subtopic_ids).delete()

        # Delete topics not in payload
        TopicModel.objects.filter(course=course_instance).exclude(id__in=incoming_topic_ids).delete()
