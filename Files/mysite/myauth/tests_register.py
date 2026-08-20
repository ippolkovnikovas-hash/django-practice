from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from myauth.models import Profile


class RegisterViewTestCase(TestCase):
    def test_register_creates_profile_and_logs_in(self):
        response = self.client.post(
            reverse("myauth:register"),
            {
                "username": "newbie",
                "password1": "SuperStrongPass123",
                "password2": "SuperStrongPass123",
            },
        )
        user = User.objects.get(username="newbie")
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(str(self.client.session.get("_auth_user_id")), str(user.pk))