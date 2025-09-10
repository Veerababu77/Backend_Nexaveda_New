
from datetime import date, timedelta
from rest_framework import serializers
from Nexaveda_user.models.attendence_model import AttendenceModel
from Nexaveda_user.models.my_courses_model import MyCoursesModel
from rest_framework.exceptions import ValidationError


class AttendenceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only = True)
    coursename = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = AttendenceModel
        fields = ['id','created_at', 'username', 'coursename']
        
    def get_username(self, obj):
        return obj.user.username if obj.user.username else None
    def get_mycourse(self,user):
        today = date.today()
        mycourse = None
        for course in MyCoursesModel.objects.filter(user = user, completion__lt = 100):
            end_date = course.created_at + timedelta(course.course.duration_in_days)
            if course.created_at.date() <= today <= end_date:
                return course
        return None
    
    def get_coursename(self,obj):
        user = obj.user
        mycourse = self.get_mycourse(user)
        return mycourse.course.course_name if mycourse else None
    
    def create(self, validated_data):
        user = validated_data.get('user')
        mycourse_active = self.get_mycourse(user)
        if mycourse_active:
            return super().create(validated_data)
        raise ValidationError("User does not have an active course based on course duration.")
            
            
            
        
    