from django.urls import reverse
from rest_framework.test import APITestCase
from tasks.models import Task
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()

class TaskAPITestCase(APITestCase):
  def setUp(self):
    self.authenticated_user = User.objects.create_user(
      username="user",
      password="pass123"
    )

    self.normal_user = User.objects.create_user(
      username="other",
      password="pass123"
    )

    self.task = Task.objects.create(
      user=self.authenticated_user,
      title="this is a test",
      description="this is a test description",
      status="pending",
      priority="high_priority",
    )

    self.url = reverse("task-list")

  def test_authenticated_user_can_access_tasks(self):

    self.client.force_authenticate(user=self.authenticated_user)

    response = self.client.get(self.url)

    self.assertEqual(response.status_code, 200)

    self.assertEqual(response.data["results"][0]['title'], "this is a test")


  def test_unauthenticated_user_cannot_access_tasks(self):

    response = self.client.get(self.url)

    self.assertEqual(response.status_code, 401)

  