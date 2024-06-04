from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def product_list(request, category_identifier=None):
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
    product = get_object_or_404(Product, id=id, identifier=identifier, available=True)
    return render(request, "market/product/detail.html", {"product": product})
