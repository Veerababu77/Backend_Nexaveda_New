import uuid
from django.db import models
from Nexaveda_user.models.courses_model import CoursesModel
from utils.helper import TimeStampModel
from django.core.validators import MinValueValidator, MaxValueValidator

class MyCoursesModel(TimeStampModel):
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, editable = False, primary_key = True)
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'mycourse_user')
    course = models.ForeignKey(CoursesModel, on_delete = models.CASCADE, related_name = 'mycourse')
    completion = models.IntegerField(default = 0, validators = [MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"
    