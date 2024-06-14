from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Form class to create a new order.

    The CreateOrderForm class inherits from the ModelForm class provided by Django.
    The form is based on the Order model.
    The fields displayed in the form are specified in the Meta class.
    """

    class Meta:
        """
        Meta class to specify the model and fields for the form.

        The model is set to Order.
        The fields displayed in the form are first_name, last_name, email, address, postal_code, and city.
        """

        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
