from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from PIL import Image
from uuid import uuid4

import io


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

    def __str__(self):
        """
        Returns the string representation of the category.

        Returns:
            str: The string representation of the category.
        """
        return self.name

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
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=False)
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

    def __str__(self):
        """
        Returns the string representation of the product.

        Returns:
            str: The string representation of the product.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to access a particular product instance.

        Returns:
            str: The URL to access a particular product instance.
        """

        return reverse("market:product_detail", args=[self.id, self.identifier])

    def save(self, *args, **kwargs):
        """
        Saves the model instance.
        Resizes the image if necessary.
        Calls the "real" save() method.
        Updates the image field.
        Raises an exception if an error occurs.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        # Determine if the image needs to be resized
        if self._state.adding:
            # This is a new product, so resize the image
            original_image = self.image
        else:
            # This is an existing product, check if the image has changed
            if self.image and self.image != self._old_image:
                original_image = self.image
            else:
                # No image change detected, skip resizing
                return

        # Call the "real" save() method to save the initial state of the model
        super(Product, self).save(*args, **kwargs)

        if original_image:
            try:
                # Open the image file in memory
                img = Image.open(original_image.path)
                # Define the desired size and aspect ratio
                max_width = 300  # Adjusted for better display in cards
                max_height = 300  # Adjusted for a 1:1 aspect ratio
                aspect_ratio = max_width / max_height

                # Calculate the new dimensions based on the aspect ratio
                width, height = img.size
                if width > height:
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)

                # Resize the image
                resized_img_io = io.BytesIO()
                img.resize((new_width, new_height), Image.ANTIALIAS)
                img.save(resized_img_io, format="JPEG")

                # Create a new content file with the resized image
                new_image = ContentFile(
                    resized_img_io.getvalue(), name=original_image.name
                )

                # Replace the original image with the resized one
                self.image.save(original_image.name, new_image, save=False)
                self.save()  # Save again to update the image field
            except Exception as e:
                print(f"Error processing image {e}")
