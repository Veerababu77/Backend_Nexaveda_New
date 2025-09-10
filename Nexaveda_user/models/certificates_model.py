
import uuid
from utils.helper import TimeStampModel
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Certificates(TimeStampModel):
    
    id = models.UUIDField(default = uuid.uuid4, primary_key = True, unique = True, editable = False)
    course = models.ForeignKey('CoursesModel', on_delete = models.CASCADE, related_name = 'course_certificate')
    issued_on = models.DateField(auto_now_add = True)
    avg_score = models.IntegerField(default = 0, validators = [MinValueValidator(0), MaxValueValidator(100)])
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'user_certificate')
    performance = models.CharField(max_length = 50, default = 'PASS')
    certificate = models.FileField(upload_to = 'certificates/', null= True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"
    
    def set_performance(self):
        if self.avg_score >= 90:
            self.performance = "OUTSTANDING"
        elif self.avg_score >= 80:
            self.performance = "BETTER"
        elif self.avg_score >= 70:
            self.performance = "PASS"
        else:
            self.performance = "FAIL"
        
    def save(self, *args, **kwargs):
        self.set_performance()
        super().save(*args, **kwargs)