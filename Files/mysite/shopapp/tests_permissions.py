from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product


class ProductPermissionsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="author", password="pass12345")
        cls.author.user_permissions.add(
            Permission.objects.get(codename="add_product"),
            Permission.objects.get(codename="change_product"),
        )
        cls.stranger_with_perm = User.objects.create_user(username="stranger", password="pass12345")
        cls.stranger_with_perm.user_permissions.add(
            Permission.objects.get(codename="change_product"),
        )
        cls.no_perm_user = User.objects.create_user(username="noperm", password="pass12345")
        cls.superuser = User.objects.create_superuser(username="admin", password="pass12345")
        cls.product = Product.objects.create(
            name="Locked Product", price=100, created_by=cls.author,
        )

    def test_create_forbidden_without_permission(self):
        self.client.force_login(self.no_perm_user)
        response = self.client.post(
            reverse("shopapp:product_create"),
            {"name": "X", "price": "1", "description": "", "discount": 0},
        )
        self.assertEqual(response.status_code, 403)

    def test_create_sets_created_by_to_current_user(self):
        self.client.force_login(self.author)
        self.client.post(
            reverse("shopapp:product_create"),
            {"name": "Authored Product", "price": "10", "description": "", "discount": 0},
        )
        product = Product.objects.get(name="Authored Product")
        self.assertEqual(product.created_by, self.author)

    def test_update_forbidden_for_stranger_with_permission(self):
        self.client.force_login(self.stranger_with_perm)
        response = self.client.get(
            reverse("shopapp:product_update", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_forbidden_for_author_without_permission(self):
        self.client.force_login(self.no_perm_user)
        self.product.created_by = self.no_perm_user
        self.product.save()
        response = self.client.get(
            reverse("shopapp:product_update", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_allowed_for_superuser_regardless_of_author(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("shopapp:product_update", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_allowed_for_author_with_permission(self):
        self.client.force_login(self.author)
        response = self.client.get(
            reverse("shopapp:product_update", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)