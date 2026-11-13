"""
server.py
Same job as these Java files:
  - ProductImpl.java  -> class ProductImpl
  - ServerImpl.java   -> class ServerImpl
  - Server.java       -> the main() part that starts everything

Steps (same as Java RMI):
  1. Make the remote objects.
  2. Start a server (Pyro5 Daemon) - like UnicastRemoteObject.
  3. Register the objects in the Name Server - like the RMI Registry.
  4. Wait for clients.
"""

import Pyro5.api
import Pyro5.nameserver

from product import Product

# Use one loop for both the Name Server and our objects.
Pyro5.config.SERVERTYPE = "multiplex"


# ---------- ProductImpl.java ----------
@Pyro5.api.expose
class ProductImpl(Product):
    """The real product object that lives on the server."""

    def __init__(self, name, description, price):
        self._name = name
        self._description = description
        self._price = price

    def get_name(self):
        print(f"[SERVER] get_name() called on {self._name}")
        return self._name

    def get_description(self):
        print(f"[SERVER] get_description() called on {self._name}")
        return self._description

    def get_price(self):
        print(f"[SERVER] get_price() called on {self._name}")
        return self._price


# ---------- ServerImpl.java ----------
@Pyro5.api.expose
class ServerImpl:
    """
    The main remote object. The client asks it for products.
    It keeps a list of products and gives back the names
    so the client can look them up.
    """

    def __init__(self, daemon):
        self.daemon = daemon
        self.products = {}

    def add_product(self, product):
        # Register each product with the daemon so it can be
        # called from far away (like exporting it in Java).
        uri = self.daemon.register(product)
        self.products[product._name] = uri
        print(f"[SERVER] Product ready: {product._name}")

    def get_product_names(self):
        print("[SERVER] get_product_names() called")
        return list(self.products.keys())

    def get_product(self, name):
        """Return the remote address (URI) of one product."""
        print(f"[SERVER] get_product('{name}') called")
        uri = self.products.get(name)
        if uri is None:
            raise ValueError(f"No product named '{name}'")
        return str(uri)


# ---------- Server.java ----------
def main():
    host = "localhost"

    # Start the Name Server (like running "rmiregistry").
    ns_uri, ns_daemon, _ = Pyro5.nameserver.start_ns(host=host, port=9090)
    print(f"[SERVER] Name Server started at {ns_uri}")

    # Make the daemon that will hold our remote objects.
    daemon = Pyro5.api.Daemon(host=host)

    # Make the server object and add some products.
    server = ServerImpl(daemon)
    server.add_product(ProductImpl("Toaster", "Makes bread crispy", 29.99))
    server.add_product(ProductImpl("Microwave", "Heats food fast", 89.50))
    server.add_product(ProductImpl("Blender", "Mixes fruit into juice", 45.00))

    # Register the server object and bind its name
    # (like Naming.rebind("rmi://localhost/ProductServer", server)).
    server_uri = daemon.register(server)
    ns_daemon.nameserver.register("example.ProductServer", server_uri)
    print(f"[SERVER] ProductServer bound as 'example.ProductServer'")
    print(f"[SERVER] URI: {server_uri}")
    print("[SERVER] Waiting for clients... (press Ctrl+C to stop)")

    # Run both daemons in one loop.
    daemon.combine(ns_daemon)
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        daemon.close()
        ns_daemon.close()


if __name__ == "__main__":
    main()
