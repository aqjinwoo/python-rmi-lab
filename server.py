"""
server.py
Same job as these Java files:
  - ProductImpl.java -> class ProductImpl
  - Server.java      -> main()
  - ServerImpl.java  -> (this file is empty in the Java project,
                         so there is nothing to translate)

Steps (same as Server.java):
  1. Make 4 product objects.
  2. Export them so they can be called from the network
     (like UnicastRemoteObject.exportObject).
  3. Bind them in the registry with a name
     (like registry.bind("laptop", stub1)).
  4. Wait for clients.
"""

import Pyro5.api
import Pyro5.nameserver

from product import Product

# Use one loop for both the Name Server (registry) and our objects.
Pyro5.config.SERVERTYPE = "multiplex"

HOST = "127.0.0.1"
REGISTRY_PORT = 9000


# ---------- ProductImpl.java ----------
@Pyro5.api.expose
class ProductImpl(Product):
    """Implements all the methods defined in the Product interface."""

    def __init__(self, new_name, new_description, new_price):
        self.name = new_name
        self.description = new_description
        self.price = new_price

    def get_name(self):
        print(f"[SERVER] get_name() called on {self.name}")
        return self.name

    def get_description(self):
        print(f"[SERVER] get_description() called on {self.name}")
        return self.description

    def get_price(self):
        print(f"[SERVER] get_price() called on {self.name}")
        return self.price


# ---------- Server.java ----------
def main():
    print("Server is booting....")

    # Start the registry (like running "rmiregistry 9000").
    ns_uri, ns_daemon, _ = Pyro5.nameserver.start_ns(host=HOST, port=REGISTRY_PORT)
    registry = ns_daemon.nameserver
    print(f"Registry started at {HOST}:{REGISTRY_PORT}")

    # We create objects from the ProductImpl class.
    p1 = ProductImpl("Laptop", "Lenovo laptop", 800000.0)
    p2 = ProductImpl("Mobile", "MI 9 mobile", 24000.0)
    p3 = ProductImpl("Bag", "Branded bag", 800.0)
    p4 = ProductImpl("Charger", "MI Charger", 230.0)

    # Export all p1, p2, p3 and p4 objects before registering them.
    daemon = Pyro5.api.Daemon(host=HOST)
    stub1 = daemon.register(p1)
    stub2 = daemon.register(p2)
    stub3 = daemon.register(p3)
    stub4 = daemon.register(p4)

    # Register the exported objects in the registry so the client
    # can look them up and call their methods.
    registry.register("laptop", stub1)
    registry.register("ram", stub2)
    registry.register("bag", stub3)
    registry.register("charger", stub4)
    print("Objects bound: laptop, ram, bag, charger")
    print("Server is ready. Waiting for clients... (press Ctrl+C to stop)")

    daemon.combine(ns_daemon)
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print("Server error", e)
    finally:
        daemon.close()
        ns_daemon.close()


if __name__ == "__main__":
    main()
