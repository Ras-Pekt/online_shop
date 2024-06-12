from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from market.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity.

    Args:
        request (HttpRequest): The request object.
        product_id (int): The product ID.
    Returns:
        HttpResponseRedirect: The cart detail page.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(product=product, quantity=cleaned_data["quantity"])

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.

    Args:
        request (HttpRequest): The request object.
        product_id (int): The product ID.
    Returns:
        HttpResponseRedirect: The cart detail page.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect("cart:cart_detail")


def cart_detail(request):
    """
    Display all items in the cart.

    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: The response object.
    """

    # cart = Cart(request)
    # return render(request, 'cart/detail.html', {'cart': cart})

    cart = Cart(request)

    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"]}
        )

    return render(request, "cart/detail.html", {"cart": cart})
