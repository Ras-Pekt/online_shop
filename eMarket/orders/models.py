from django.db import models
from market.models import Product


class Order(models.Model):
    """
    Order model to store order information.

    The Order model has the following fields:
    - first_name: the first name of the customer
    - last_name: the last name of the customer
    - email: the email address of the customer
    - address: the address of the customer
    - postal_code: the postal code of the customer
    - city: the city of the customer
    - created: the date and time the order was created
    - updated: the date and time the order was last updated
    - paid: a boolean field to indicate if the order has been paid for
    - items: a many-to-many relationship with the Product model to store the products in the order
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        """
        Meta class to define the ordering of the Order objects and create an index on the created field for faster lookups.

        The ordering is set to descending order based on the created field.
        An index is created on the created field for faster lookups.
        """

        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        """
        Method to return a string representation of the Order object.
        The string representation includes the Order ID.
        """
        return f"Order ID: {self.id}"

    def get_total_cost(self):
        """
        Method to calculate the total cost of the order.
        The total cost is calculated by summing the cost of all the products in the order.
        """
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    OrderItem model to store information about the products in an order.

    The OrderItem model has the following fields:
    - order: a foreign key to the Order model to associate the order item with an order
    - product: a foreign key to the Product model to associate the order item with a product
    - price: the price of the product at the time of the order
    - quantity: the quantity of the product in the order
    """

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Method to return a string representation of the OrderItem object.
        The string representation includes the product name and the quantity.
        """
        # return str(self.id)
        return f"{self.product.name} x {self.quantity}"

    def get_cost(self):
        """
        Method to calculate the cost of the order item.
        The cost is calculated by multiplying the price of the product by the quantity.
        """
        return self.price * self.quantity
