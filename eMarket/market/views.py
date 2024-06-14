from cart.forms import CartAddProductForm
from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def product_list(request, category_identifier=None):
    """
    List of products view.

    Args:
        request (HttpRequest): The request object.
        category_identifier (str): The category identifier.
    Returns:
        HttpResponse: The HTTP response.
    """

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_identifier:
        category = get_object_or_404(Category, identifier=category_identifier)
        products = products.filter(category=category)
    return render(
        request,
        "market/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, identifier):
    """
    Product detail view.

    Args:
        request (HttpRequest): The request object.
        id (str): The product ID.
        identifier (str): The product identifier.
    Returns:
        HttpResponse: The HTTP response.
    """

    product = get_object_or_404(Product, id=id, identifier=identifier, available=True)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "market/product/detail.html",
        {"product": product, "cart_product_form": cart_product_form},
    )
