from django.db import models
from uuid import uuid4


class Category(models.Model):
    # TODO: implement a custom id field that uses the uuid module

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    identifier = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

        def __str__(self):
            return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    identifier = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'identifier']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

        def __str__(self):
            return self.name
