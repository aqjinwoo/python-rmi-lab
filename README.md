# Python RMI Lab (Pyro5)

This project takes the idea of a **Java RMI** (Remote Method Invocation) project and builds the same thing in **Python** using **Pyro5** (Python Remote Objects).

This is a Python version of the Java project here:
https://github.com/nix1947/sunway_dpp/tree/master/JAVA_RMI_IV

The server makes 4 products (Laptop, Mobile, Bag, Charger) and puts them in a registry. The client looks up the `laptop` object and calls its methods over the network as if it were a normal local object.

## Files

| Python file  | Java file(s) it replaces | What it does |
|--------------|--------------------------|--------------|
| `product.py` | `Product.java`           | The remote interface. Lists the methods a product must have: `get_name()`, `get_description()`, `get_price()`. |
| `server.py`  | `ProductImpl.java`, `Server.java`, `ServerImpl.java` | Makes the 4 products, starts the registry on `127.0.0.1:9000`, and binds them as `laptop`, `ram`, `bag`, `charger`. (`ServerImpl.java` is empty in the Java project.) |
| `client.py`  | `Client.java`            | Looks up `laptop` in the registry and prints its name, description and price. |

## Java RMI vs Pyro5

| Java RMI                                   | Pyro5 (Python)                          |
|--------------------------------------------|-----------------------------------------|
| `interface Product extends Remote`         | `class Product(ABC)`                    |
| `UnicastRemoteObject.exportObject(p1, 0)`  | `daemon.register(p1)`                   |
| `rmiregistry 9000`                         | Pyro5 Name Server on port 9000          |
| `registry.bind("laptop", stub1)`           | `registry.register("laptop", stub1)`    |
| `registry.lookup("laptop")`                | `Proxy("PYRONAME:laptop@127.0.0.1:9000")` |
| Stub                                       | Proxy                                   |

## How to run

**1. Install Python 3.8 or newer**, then install Pyro5:

```
pip install -r requirements.txt
```

**2. Start the server** (Terminal 1):

```
python server.py
```

The server also starts the registry for you, so you do not need to run anything else.

**3. Run the client** (Terminal 2):

```
python client.py
```

**4. Stop the server** with `Ctrl+C` in Terminal 1.

## Expected output

**Server terminal:**

```
Server is booting....
Registry started at 127.0.0.1:9000
Objects bound: laptop, ram, bag, charger
Server is ready. Waiting for clients... (press Ctrl+C to stop)
[SERVER] get_name() called on Laptop
[SERVER] get_description() called on Laptop
[SERVER] get_price() called on Laptop
```

**Client terminal:**

```
Name:Laptop
Description: Lenovo laptop
Price: 800000.0
```

## How it works

1. `server.py` starts a registry (Pyro5 Name Server) on `127.0.0.1:9000`.
2. It makes 4 `ProductImpl` objects and exports each one with the Daemon so they can be called from the network.
3. It binds them in the registry with the names `laptop`, `ram`, `bag` and `charger`.
4. `client.py` looks up `laptop` in the registry and gets a proxy (like a Java stub).
5. The client calls `get_name()`, `get_description()` and `get_price()`. Each call runs on the server, which you can see in the server terminal.

Screenshots are in the `Screenshot` folder.
