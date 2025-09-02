
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.helper import TimeStampModel


class CoursesModel(TimeStampModel):
    """
    Model for Course we offer to the people.
    """
    CHOICE_LEVEL = [
        ("BEGINEER", "BEGINEER"),
        ("INTERMEDIATE", "INTERMEDIATE"),
        ("ADVANCED", "ADVANCED")
    ]
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, editable = False,primary_key=True)
    course_name = models.CharField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    course_pic = models.ImageField(upload_to = 'course_pic/', null = True, blank = True)
    instructor = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'instructor')
    duration_in_days = models.IntegerField(default = 60)
    course_level = models.CharField(max_length = 100, choices = CHOICE_LEVEL, default = "BEGINEER")
    course_cost = models.IntegerField(default = 3000)
    course_discount = models.IntegerField(default = 50)
    is_active = models.BooleanField(default = True)
    
    
    def __str__(self):
        return self.course_name
    
    
class TopicModel(TimeStampModel):
    """
    Model for topics for each Course.
    """
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, editable = False, primary_key=True)
    title = models.CharField(max_length = 255)
    course = models.ForeignKey(CoursesModel, on_delete = models.CASCADE, related_name = 'topics')
    
    def __str__(self):
        return f"{self.course.course_name} - {self.title}"
    
class SubtopicModel(TimeStampModel):
    """
    Model Subtopics for each course
    """
    id = models.UUIDField(default = uuid.uuid4, unique = True, editable = False, primary_key=True)
    subtopic = models.CharField(max_length = 255)
    topics =  models.ForeignKey(TopicModel, on_delete = models.CASCADE, related_name = 'subtopic')
    
    def __str__(self):
        return f"{self.topics.title} - {self.subtopic}"
    
class RatingModel(TimeStampModel):
    """This Model will calculate rating of Course"""
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, editable = False, primary_key = True)
    rating = models.IntegerField(default = 0, validators = [MinValueValidator(0), MaxValueValidator(5)])
    course = models.ForeignKey(CoursesModel, on_delete = models.CASCADE, related_name = 'courses')
    
    def __str__(self):
        return f"{self.course.course_name}"
    
    