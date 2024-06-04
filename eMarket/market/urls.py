from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path(
        "<slug:category_identifier>/",
        views.product_list,
        name="product_list_by_category",
    ),
    path("<uuid:id>/<slug:identifier>/", views.product_detail, name="product_detail"),
]
