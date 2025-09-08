
import uuid
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from Nexaveda_user.models.courses_model import CoursesModel, TopicModel, SubtopicModel, RatingModel

User = get_user_model()
class CourseTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email = "course@gmail.com",
            password = "Course@9848"
        )
        self.client.force_authenticate(user=self.user)
        
        self.course = CoursesModel.objects.create(
            course_name="setupcourse",
            description="setup description",
            duration_in_days=15,
            course_level="BEGINEER",
            course_cost=500,
            course_discount=5,
            is_active=True,
            instructor=self.user
        )
        
        self.topic = TopicModel.objects.create(
            title = "Topictitle",
            course = self.course
        )
        
        self.subtopic = SubtopicModel.objects.create(
            subtopic = "SubtopicExample",
            topics = self.topic
        )
        
        self.course_url = reverse("Nexaveda_user:course")
        self.course_detail_url = reverse("Nexaveda_user:course-detail", kwargs={"id":str(self.course.id)})
        
        self.topic_url = reverse("Nexaveda_user:topic", kwargs = {"course_id" : str(self.course.id)})
        self.topic_detail_url = reverse("Nexaveda_user:topic-detail", kwargs = {"id":str(self.topic.id)})
        
        self.subtopic_url = reverse("Nexaveda_user:subtopic", kwargs = {"topic_id":str(self.topic.id)})
        self.subtopic_detail_url = reverse("Nexaveda_user:sub-topic-detail", kwargs = {"id":str(self.subtopic.id)})
        
        self.rating_url = reverse("Nexaveda_user:rating", kwargs= {"course_id":str(self.course.id)})
        
    def test_course_post(self):
        response = self.client.post(self.course_url, {
            "course_name" : "examplecourse",
            "description" : "exampledescription",
            "instructor" : self.user.id,
            "course_discount": 10,
            "course_cost": 1000,
            "duration_in_days": 30,
            "course_level": "BEGINEER",
            "is_active": True,
        }, format = "json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["course_name"], "examplecourse")
        
    def test_course_patch(self):
        response = self.client.patch(self.course_detail_url, {
            "description" : "description",
            "course_discount" : 25
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["description"], "description")
        self.assertEqual(response.data["data"]["course_discount"], 25)
        
    def test_topic_post(self):
        response = self.client.post(self.topic_url,{
            "title" : "ExampleTitle",
            "course" : self.course.id
        }, format = "json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_topic_patch(self):
        response = self.client.patch(self.topic_detail_url,{
            "title":"Topictitle - 2"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"],"Topictitle - 2")
        
    def test_subtopic_post(self):
        response = self.client.post(self.subtopic_url, {
            "subtopic" : "Subtopic",
            "topics" : self.topic.id
        }, format = "json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["subtopic"], "Subtopic")
        
    def test_subtopic_patch(self):
        response = self.client.patch(self.subtopic_detail_url, {
            "subtopic" : "subbb"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["subtopic"], "subbb")
        
    def test_invalid_subtopic_id(self):
        invalid_id = str(uuid.uuid4())
        url = reverse("Nexaveda_user:sub-topic-detail", kwargs = {"id": invalid_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_rating_post(self):
        rating_sample = {
            "rating" : 5,
            "course" : self.course.id,
            "user" : self.user.id
        }
        response = self.client.post(self.rating_url, rating_sample , format = "json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],"Rating created")
    
    def test_rating_patch(self):
        RatingModel.objects.create(
            rating = 4,
            course = self.course,
            user = self.user
        )
        response = self.client.post(self.rating_url,{
            "rating" : 5,
            "course" : self.course.id,
            "user" : self.user.id,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],"Rating updated")
        
    def test_subtopic_delete(self):
        response = self.client.delete(self.subtopic_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], "Sub topic deleted successfully")
        
    def test_topic_delete(self):
        response = self.client.delete(self.topic_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Topic deleted succesfully")
        
    def test_course_delete(self):
        response = self.client.delete(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.is_active, False)
        