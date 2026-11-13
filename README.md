# Python RMI Lab (Pyro5)

This project takes the idea of a **Java RMI** (Remote Method Invocation) project and builds the same thing in **Python** using **Pyro5** (Python Remote Objects).

The server keeps a list of products. The client connects over the network, asks for the products, and calls methods on them as if they were normal local objects.

## Files

| Python file  | Java file(s) it replaces                      | What it does |
|--------------|-----------------------------------------------|--------------|
| `product.py` | `Product.java`                                | The remote interface. Lists the methods a product must have. |
| `server.py`  | `ProductImpl.java`, `ServerImpl.java`, `Server.java` | Makes the products, starts the Name Server, and waits for clients. |
| `client.py`  | `Client.java`                                 | Finds the server, gets the products, and prints their details. |

## Java RMI vs Pyro5

| Java RMI                          | Pyro5 (Python)                       |
|-----------------------------------|--------------------------------------|
| `interface Product extends Remote`| `class Product(ABC)`                 |
| `UnicastRemoteObject`             | `@Pyro5.api.expose` + `Daemon`       |
| `rmiregistry`                     | Pyro5 Name Server                    |
| `Naming.rebind(...)`              | `nameserver.register(...)`           |
| `Naming.lookup(...)`              | `Proxy("PYRONAME:...")`              |
| Stub                              | Proxy                                |
| `RemoteException`                 | Error is sent back to the client     |

## How to run

**1. Install Python 3.8 or newer**, then install Pyro5:

```
pip install -r requirements.txt
```

**2. Start the server** (Terminal 1):

```
python server.py
```

Wait until you see:

```
[SERVER] Waiting for clients... (press Ctrl+C to stop)
```

The server also starts the Name Server for you, so you do not need to run anything else.

**3. Run the client** (Terminal 2):

```
python client.py
```

**4. Stop the server** with `Ctrl+C` in Terminal 1.

## Expected output

**Client terminal:**

```
[CLIENT] Looking up 'example.ProductServer' ...
[CLIENT] Found 3 products: ['Toaster', 'Microwave', 'Blender']

[CLIENT] Name:        Toaster
[CLIENT] Description: Makes bread crispy
[CLIENT] Price:       $29.99
----------------------------------------
...
[CLIENT] Error from server: No product named 'Television'
[CLIENT] Done.
```

**Server terminal:**

```
[SERVER] Name Server started at PYRO:Pyro.NameServer@localhost:9090
[SERVER] Product ready: Toaster
[SERVER] Product ready: Microwave
[SERVER] Product ready: Blender
[SERVER] ProductServer bound as 'example.ProductServer'
[SERVER] Waiting for clients... (press Ctrl+C to stop)
[SERVER] get_product_names() called
[SERVER] get_product('Toaster') called
[SERVER] get_name() called on Toaster
...
```

## How it works

1. `server.py` starts a **Name Server** on port 9090. This is like the RMI Registry.
2. It makes three `ProductImpl` objects and registers each one with the **Daemon**, so they can be called from the network.
3. It registers the `ServerImpl` object in the Name Server with the name `example.ProductServer`.
4. `client.py` looks up `example.ProductServer` in the Name Server and gets a **proxy** (like a Java stub).
5. The client asks for the product names, then gets a proxy for each product and calls `get_name()`, `get_description()` and `get_price()`.
6. Every call runs on the server. You can see this in the server terminal.

