from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
import json


# class LoginViewTestCase(TestCase):
#     def setUp(self):
#         self.username = "testuser"
#         self.password = "TestPass123!"
#         self.user = User.objects.create_user(
#             username=self.username,
#             password=self.password,
#         )

#     def test_login_page_get_returns_200(self):
#         response = self.client.get(reverse("myauth:login"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "myauth/login.html")
#
#     def test_login_page_redirects_if_already_authenticated(self):
#         self.client.login(username=self.username, password=self.password)
#         response = self.client.get(reverse("myauth:login"))
#         self.assertEqual(response.status_code, 302)
#
#     def test_successful_login_redirects(self):
#         response = self.client.post(
#             reverse("myauth:login"),
#             {"username": self.username, "password": self.password},
#         )
#         self.assertEqual(response.status_code, 302)
#         user_id = self.client.session.get("_auth_user_id")
#         self.assertEqual(str(user_id), str(self.user.pk))
#
#     def test_login_with_wrong_password_fails(self):
#         response = self.client.post(
#             reverse("myauth:login"),
#             {"username": self.username, "password": "wrong-password"},
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn("_auth_user_id", self.client.session)
#
#
# class LogoutViewTestCase(TestCase):
#     def setUp(self):
#         self.username = "testuser"
#         self.password = "TestPass123!"
#         self.user = User.objects.create_user(
#             username=self.username,
#             password=self.password,
#         )
#
#     def test_logout_get_not_allowed(self):
#         # Начиная с Django 4.1/5.0 LogoutView принимает только POST
#         self.client.login(username=self.username, password=self.password)
#         response = self.client.get(reverse("myauth:logout"))
#         self.assertEqual(response.status_code, 405)
#
#     def test_logout_post_redirects_to_login(self):
#         self.client.login(username=self.username, password=self.password)
#         response = self.client.post(reverse("myauth:logout"))
#         self.assertRedirects(
#             response,
#             reverse("myauth:login"),
#             fetch_redirect_response=False,
#         )
#
#     def test_logout_actually_ends_session(self):
#         self.client.login(username=self.username, password=self.password)
#         self.client.post(reverse("myauth:logout"))
#         self.assertNotIn("_auth_user_id", self.client.session)
#
#
# class CookieViewsTestCase(TestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser(username="admin_cookie", password="pass12345")
#
#     def test_set_cookie_view_sets_cookie(self):
#         self.client.force_login(self.superuser)
#         response = self.client.get(reverse("myauth:set_cookie_view"))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("fizz", response.cookies)
#         self.assertEqual(response.cookies["fizz"].value, "buzz")
#
#     def test_get_cookie_view_returns_default_when_missing(self):
#         response = self.client.get(reverse("myauth:get_cookie_view"))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("default value", response.content.decode())
#
#     def test_get_cookie_view_returns_actual_value_when_present(self):
#         self.client.cookies["fizz"] = "buzz"
#         response = self.client.get(reverse("myauth:get_cookie_view"))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("buzz", response.content.decode())
#
#
# class SessionViewsTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="session_user", password="pass12345")
#         self.user.user_permissions.add(Permission.objects.get(codename="view_profile"))
#         self.client.force_login(self.user)
#
#     def test_set_session_view_sets_value(self):
#         response = self.client.get(reverse("myauth:session-set"))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.client.session.get("foobar"), "spameggs")
#
#     def test_get_session_view_returns_default_when_missing(self):
#         response = self.client.get(reverse("myauth:session-get"))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("default value", response.content.decode())
#
#     def test_get_session_view_returns_actual_value_after_set(self):
#         self.client.get(reverse("myauth:session-set"))
#         response = self.client.get(reverse("myauth:session-get"))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("spameggs", response.content.decode())
#
#
# class UrlNamesTestCase(TestCase):
#     def test_all_named_urls_resolve(self):
#         names = [
#             "myauth:login", "myauth:logout", "myauth:get_cookie_view",
#             "myauth:set_cookie_view", "myauth:session-set", "myauth:session-get",
#         ]
#         for name in names:
#             with self.subTest(name=name):
#                 url = reverse(name)
#                 self.assertTrue(url.startswith("/accounts/"))

# python manage.py test myauth.tests

class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:get_cookie_view'))
        self.assertContains(response, "Cookie value")

class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse('myauth:foo-bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["content-type"], 'application/json',
        )
        expected_data = {"foo": "bar", "spam": "eggs"}
        self.assertJSONEqual(response.content, expected_data)