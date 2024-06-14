from decimal import Decimal
from django.conf import settings
from market.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart.

        Args:
            request (HttpRequest): The request object.
        Returns:
            None
        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session[settings.CART_SESSION_ID]

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        # def add(self, product, quantity=1):
        """Add a product to the cart or update its quantity.

        Args:
            product (Product): The product to add.
            quantity (int): The quantity of the product.
            update_quantity (bool): A flag to update the quantity.
        Returns:
            None
        """

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        # if product_id not in self.cart:
        #     self.cart[product_id] = {"quantity": quantity, "price": str(product.price)}
        # else:
        #     self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        """Save the cart."""

        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart.

        Args:
            product (Product): The product to remove.
        """

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.

        Yields:
            dict: The product information.
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Custom len() method to count all items in the cart.

        Returns:
            int: The total number of items in the cart.
        """

        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Get the total price of the items in the cart.

        Returns:
            Decimal: The total price of the items in the cart.
        """

        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """
        Remove the cart from the session.
        """

        del self.session[settings.CART_SESSION_ID]
        self.save()
