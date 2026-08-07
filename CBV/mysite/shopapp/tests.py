from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order, Product


class ProductViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="tester", password="pass12345")
        cls.active_product = Product.objects.create(
            name="Active Product",
            price=100,
            description="desc",
            discount=10,
            archived=False,
        )
        cls.archived_product = Product.objects.create(
            name="Archived Product",
            price=200,
            description="desc archived",
            discount=0,
            archived=True,
        )

    def test_products_list_status_ok(self):
        response = self.client.get(reverse("shopapp:products_list"))
        self.assertEqual(response.status_code, 200)

    def test_products_list_shows_only_non_archived(self):
        response = self.client.get(reverse("shopapp:products_list"))
        products = list(response.context["products"])
        self.assertIn(self.active_product, products)
        self.assertNotIn(self.archived_product, products)

    def test_products_list_contains_detail_link(self):
        response = self.client.get(reverse("shopapp:products_list"))
        detail_url = reverse(
            "shopapp:products_details", kwargs={"pk": self.active_product.pk}
        )
        self.assertContains(response, detail_url)

    def test_product_detail_status_ok(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.active_product.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], self.active_product)

    def test_product_detail_404_for_missing_pk(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_product_create_get_form(self):
        response = self.client.get(reverse("shopapp:product_create"))
        self.assertEqual(response.status_code, 200)

    def test_product_create_post_creates_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": "New Product",
                "price": "150.00",
                "description": "brand new",
                "discount": 5,
            },
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name="New Product").exists())

    def test_product_update_get_prefilled_form(self):
        response = self.client.get(
            reverse("shopapp:product_update", kwargs={"pk": self.active_product.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.active_product.name)

    def test_product_update_post_updates_product(self):
        response = self.client.post(
            reverse("shopapp:product_update", kwargs={"pk": self.active_product.pk}),
            {
                "name": "Updated Name",
                "price": "999.00",
                "description": "updated desc",
                "discount": 20,
            },
        )
        self.active_product.refresh_from_db()
        self.assertEqual(self.active_product.name, "Updated Name")
        self.assertRedirects(
            response,
            reverse("shopapp:products_details", kwargs={"pk": self.active_product.pk}),
        )

    def test_product_delete_get_confirmation_page(self):
        response = self.client.get(
            reverse("shopapp:product_delete", kwargs={"pk": self.active_product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_product_delete_post_archives_not_deletes(self):
        response = self.client.post(
            reverse("shopapp:product_delete", kwargs={"pk": self.active_product.pk})
        )
        self.active_product.refresh_from_db()
        self.assertTrue(self.active_product.archived)
        self.assertTrue(Product.objects.filter(pk=self.active_product.pk).exists())
        self.assertRedirects(response, reverse("shopapp:products_list"))


class OrderViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="buyer", password="pass12345")
        cls.product1 = Product.objects.create(name="P1", price=50)
        cls.product2 = Product.objects.create(name="P2", price=75)
        cls.order = Order.objects.create(
            delivery_address="Street 1",
            promocode="SALE10",
            user=cls.user,
        )
        cls.order.products.set([cls.product1, cls.product2])

    def setUp(self):
        self.client.login(username="buyer", password="pass12345")

    def test_orders_list_status_ok(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 200)

    def test_orders_list_shows_user_and_products(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "buyer")
        self.assertContains(response, "P1")
        self.assertContains(response, "P2")

    def test_orders_list_contains_detail_link(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        detail_url = reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        self.assertContains(response, detail_url)

    def test_order_detail_status_ok(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_order_detail_shows_user_and_products(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertContains(response, "buyer")
        self.assertContains(response, "P1")
        self.assertContains(response, "P2")

    def test_order_detail_has_update_and_delete_links(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        update_url = reverse("shopapp:order_update", kwargs={"pk": self.order.pk})
        delete_url = reverse("shopapp:order_delete", kwargs={"pk": self.order.pk})
        self.assertContains(response, update_url)
        self.assertContains(response, delete_url)

    def test_order_create_get_form(self):
        response = self.client.get(reverse("shopapp:order_create"))
        self.assertEqual(response.status_code, 200)

    def test_order_create_post_creates_order_with_current_user(self):
        response = self.client.post(
            reverse("shopapp:order_create"),
            {
                "delivery_address": "New Street 5",
                "promocode": "WELCOME",
                "products": [self.product1.pk],
            },
        )
        self.assertRedirects(response, reverse("shopapp:orders_list"))
        new_order = Order.objects.get(promocode="WELCOME")
        self.assertEqual(new_order.user, self.user)
        self.assertIn(self.product1, new_order.products.all())

    def test_order_update_get_prefilled_form(self):
        response = self.client.get(
            reverse("shopapp:order_update", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SALE10")

    def test_order_update_post_updates_order(self):
        response = self.client.post(
            reverse("shopapp:order_update", kwargs={"pk": self.order.pk}),
            {
                "delivery_address": "Updated Street",
                "promocode": "SALE10",
                "products": [self.product2.pk],
            },
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.delivery_address, "Updated Street")
        self.assertRedirects(
            response,
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk}),
        )

    def test_order_delete_get_confirmation_page(self):
        response = self.client.get(
            reverse("shopapp:order_delete", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_order_delete_post_fully_deletes(self):
        order_pk = self.order.pk
        response = self.client.post(
            reverse("shopapp:order_delete", kwargs={"pk": order_pk})
        )
        self.assertFalse(Order.objects.filter(pk=order_pk).exists())
        self.assertRedirects(response, reverse("shopapp:orders_list"))