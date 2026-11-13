"""
product.py
Same job as Product.java in the Java RMI project.

In Java, Product is a "remote interface". It lists the methods
a client is allowed to call on a product that lives on the server.

Python does not have interfaces like Java, so we use an
abstract base class (ABC) to show the same idea.
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """The remote interface for a product."""

    @abstractmethod
    def get_name(self):
        """Return the product name."""

    @abstractmethod
    def get_description(self):
        """Return a short description of the product."""

    @abstractmethod
    def get_price(self):
        """Return the product price."""
