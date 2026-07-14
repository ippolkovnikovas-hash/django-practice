from timeit import default_timer

from django.http import HttpRequest
from django.shortcuts import render

def shop_index(request: HttpRequest):
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
