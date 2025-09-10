
from rest_framework import serializers
from Nexaveda_user.models.certificates_model import Certificates

class CertificatesSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only = True)
    course_name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Certificates
        fields = ['id','username','course_name','issued_on', 'performance', 'certificate']
        
    def get_username(self, obj):
        return obj.user.username
    def course_name(self, obj):
        return obj.course.course_name
    
# class CertificatesPostSerializer(serializers.ModelSerializer):
#     class 
        