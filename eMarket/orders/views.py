from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import CreateOrderForm
from cart.cart import Cart
from django.contrib import messages


def create_order(request):
    cart = Cart(request)

    if request.method == "POST":
        form = CreateOrderForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()

            return render(request, "orders/order_created.html", {"order": order})
    else:
        form = CreateOrderForm()

    return render(request, "orders/create_order.html", {"cart": cart, "form": form})
