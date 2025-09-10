from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Nexaveda_user.models.user_model import User
from Nexaveda_user.models.courses_model import CoursesModel, TopicModel, SubtopicModel, RatingModel
from Nexaveda_user.models.certificates_model import Certificates
from Nexaveda_user.models.my_courses_model import MyCoursesModel
from Nexaveda_user.models.attendence_model import AttendenceModel

@admin.register(AttendenceModel)
class AttendenceAdmin(admin.ModelAdmin):
    list_display = ['username','course_name']
    list_filter = ['created_at']
    ordering = ['-created_at']
    
    def username(self, obj):
        return obj.user.username
    username.admin_order_field = 'user__username'
    username.short_description = 'User'
    def course_name(self,obj):
        return obj.course.course_name
    course_name.admin_order_field = 'course__course_name'
    course_name.short_description = 'Course'
@admin.register(MyCoursesModel)
class MycourseAdmin(admin.ModelAdmin):
    list_display = ['completion']

@admin.register(Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    list_display = ['username','course_name', 'issued_on','avg_score', 'performance']
    list_filter = ['issued_on']
    ordering = ['-created_at']
    
    def username(self, obj):
        return obj.user.username
    username.admin_order_field = 'user__username'
    username.short_description = 'User'
    def course_name(self,obj):
        return obj.course.course_name
    course_name.admin_order_field = 'course__course_name'
    course_name.short_description = 'Course'
@admin.register(CoursesModel)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'description', 'course_level', 'course_cost')
    list_filter = ('course_name', 'course_cost')
    ordering = ['-created_at']
    
@admin.register(TopicModel)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','created_at')
    list_filter = ('title','created_at')
    ordering = ['-created_at']
    
@admin.register(SubtopicModel)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('subtopic','created_at')
    list_filter = ('subtopic','created_at')
    ordering = ['-created_at']
    
@admin.register(RatingModel)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating','created_at')
    list_filter = ('rating','created_at')
    ordering = ['-created_at']
class UserAdmin(BaseUserAdmin):
    # Fields to display in admin list
    list_display = ('email', 'username', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    # Fields to use in the admin form for adding/changing users
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email','username')
    filter_horizontal = ('groups', 'user_permissions',)

# Register the custom user model with the admin
admin.site.register(User, UserAdmin)


