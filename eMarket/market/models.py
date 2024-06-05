from django.db import models
from django.urls import reverse
from uuid import uuid4


class Category(models.Model):
    """
    Category model.

    Attributes:
        id (UUIDField): The primary key of the model.
        name (CharField): The name of the category.
        identifier (SlugField): The identifier of the category.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    identifier = models.SlugField(max_length=200, unique=True)

    class Meta:
        """
        Meta options.

        Attributes:
            ordering (list): The default ordering of the model.
            indexes (list): The model's indexes.
            verbose_name (str): The verbose name of the model.
            verbose_name_plural (str): The verbose name of the model in plural.
        """

        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        """
        Returns the URL to access a particular category instance.

        Returns:
            str: The URL to access a particular category instance.
        """

        return reverse("market:product_list_by_category", args=[self.identifier])


class Product(models.Model):
    """
    Product model.

    Attributes:
        id (UUIDField): The primary key of the model.
        category (ForeignKey): The category of the product.
        name (CharField): The name of the product.
        identifier (SlugField): The identifier of the product.
        image (ImageField): The image of the product.
        description (TextField): The description of the product.
        price (DecimalField): The price of the product.
        available (BooleanField): The availability of the product.
        created (DateTimeField): The date and time the product was created.
        updated (DateTimeField): The date and time the product was last updated.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    identifier = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options.

        Attributes:
            ordering (list): The default ordering of the model.
            indexes (list): The model's indexes.
        """

        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "identifier"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def get_absolute_url(self):
        """
        Returns the URL to access a particular product instance.

        Returns:
            str: The URL to access a particular product instance.
        """

        return reverse("market:product_detail", args=[self.id, self.identifier])
