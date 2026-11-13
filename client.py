"""
client.py
Same job as Client.java in the Java RMI project.

Steps (same as Java RMI):
  1. Find the Name Server (like LocateRegistry / Naming.lookup).
  2. Get a proxy to the remote ProductServer (like the Java stub).
  3. Call methods on it as if it were a normal local object.
"""

import Pyro5.api


def main():
    print("[CLIENT] Looking up 'example.ProductServer' ...")

    # PYRONAME: asks the Name Server where the object is.
    with Pyro5.api.Proxy("PYRONAME:example.ProductServer@localhost:9090") as server:
        names = server.get_product_names()
        print(f"[CLIENT] Found {len(names)} products: {names}\n")

        for name in names:
            # Get a proxy (stub) for each remote product.
            product_uri = server.get_product(name)
            with Pyro5.api.Proxy(product_uri) as product:
                print(f"[CLIENT] Name:        {product.get_name()}")
                print(f"[CLIENT] Description: {product.get_description()}")
                print(f"[CLIENT] Price:       ${product.get_price():.2f}")
                print("-" * 40)

        # Show what happens with a product that does not exist.
        try:
            server.get_product("Television")
        except ValueError as e:
            print(f"[CLIENT] Error from server: {e}")

    print("[CLIENT] Done.")


if __name__ == "__main__":
    main()
