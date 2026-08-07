from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy

from .forms import ProductForm, OrderForm, GroupsForm
from .models import Product, Order
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "time_running": default_timer(),
            "products": [
                ("Desk", 999),
                ("Chair", 299),
                ("Sofa", 1999),
            ],
            "username": "admin",
        }
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest)-> HttpResponse:
        context = {
            "form": GroupsForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupsForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailView(DetailView):

    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"


class ProductsListView(ListView):

    template_name = "shopapp/products-list.html"
    #model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

class OrdersListView(ListView):
    queryset = (
        Order.objects.
        select_related("user").
        prefetch_related("products")
    )

class OrderDetailView(DetailView):
    queryset = (
        Order.objects.
        select_related("user").
        prefetch_related("products")
    )

class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:products_details",
            kwargs={"pk": self.object.pk},
        )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form: ProductForm) -> HttpResponse:
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "shopapp/order_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

