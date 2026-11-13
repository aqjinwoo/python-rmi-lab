"""
client.py
Same job as Client.java in the Java RMI project.

Steps (same as Client.java):
  1. Get the registry at 127.0.0.1:9000 (like LocateRegistry.getRegistry).
  2. Look up the "laptop" object (like registry.lookup("laptop")).
  3. Call its methods as if it were a normal local object.
"""

import Pyro5.api


def main():
    try:
        # Lookup the laptop object and assign it to the laptop variable.
        with Pyro5.api.Proxy("PYRONAME:laptop@127.0.0.1:9000") as laptop:
            laptop_name = laptop.get_name()
            laptop_description = laptop.get_description()
            price = laptop.get_price()

            print("Name:" + laptop_name)
            print("Description: " + laptop_description)
            print("Price: " + str(price))
    except Exception as e:
        print("Exception in client side", e)


if __name__ == "__main__":
    main()
