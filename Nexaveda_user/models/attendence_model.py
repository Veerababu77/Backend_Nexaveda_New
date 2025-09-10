import uuid
from django.db import models
from utils.helper import TimeStampModel


class AttendenceModel(TimeStampModel):
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'user_attendence')
    course = models.ForeignKey('CoursesModel', on_delete = models.CASCADE, related_name = 'course_attendence')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}" 