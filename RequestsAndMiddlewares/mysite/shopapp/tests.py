from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.urls import reverse

from .models import Product, Order
from .admin import ProductAdmin, mark_archived


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Desk",
            description="Wooden desk",
            price=999,
            discount=10,
        )

    def test_product_str(self):
        self.assertEqual(str(self.product.name), "Desk")

    def test_discount_is_positive(self):
        self.assertGreaterEqual(self.product.discount, 0)

    def test_default_archived_is_false(self):
        self.assertFalse(self.product.archived)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.product = Product.objects.create(name="Chair", price=299)
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="Test address 1",
        )
        self.order.products.add(self.product)

    def test_order_has_user(self):
        self.assertEqual(self.order.user.username, "tester")

    def test_order_has_products(self):
        self.assertIn(self.product, self.order.products.all())

    def test_order_products_count(self):
        self.assertEqual(self.order.products.count(), 1)


class ProductAdminSearchTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com"
        )
        self.client = Client()
        self.client.login(username="admin", password="adminpass")
        Product.objects.create(name="Sofa", price=1999)
        Product.objects.create(name="Table", price=499)

    def test_search_by_name(self):
        url = reverse("admin:shopapp_product_changelist")
        response = self.client.get(url, {"q": "Sofa"})
        self.assertContains(response, "Sofa")
        self.assertNotContains(response, "Table")

    def test_search_by_price(self):
        url = reverse("admin:shopapp_product_changelist")
        response = self.client.get(url, {"q": "1999"})
        self.assertContains(response, "Sofa")


class ProductAdminActionTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.product1 = Product.objects.create(name="Lamp", price=50, archived=False)
        self.product2 = Product.objects.create(name="Mirror", price=80, archived=False)

    def test_mark_archived_action(self):
        admin_model = ProductAdmin(Product, self.site)
        queryset = Product.objects.filter(pk__in=[self.product1.pk, self.product2.pk])
        mark_archived(admin_model, request=None, queryset=queryset)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertTrue(self.product1.archived)
        self.assertTrue(self.product2.archived)


class ProductAdminFieldsetsTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin2", password="adminpass", email="admin2@test.com"
        )
        self.client = Client()
        self.client.login(username="admin2", password="adminpass")
        self.product = Product.objects.create(name="Bed", price=1500, discount=5)

    def test_product_change_page_loads(self):
        url = reverse("admin:shopapp_product_change", args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fieldsets_present_in_page(self):
        url = reverse("admin:shopapp_product_change", args=[self.product.pk])
        response = self.client.get(url)
        self.assertContains(response, "Price options")
        self.assertContains(response, "Extra options")
