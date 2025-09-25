import base64
from uuid import uuid4
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from register_data.register import UserRegistery, ProductRegistery ,OrderRegistery, CardRegistery


class Order:
    register = OrderRegistery()
    
    def __init__(self, user, prod):
        self.user = user
        self.prod = prod
        self.exist = True
        
        if not self.prod.available:
            self.destroy()
            return
        
        self.state = "In process"
        self.id = Order.register.register_order(self)
        self.make()
        
    def cancel(self):
        self.prod.stock += 1
        self.prod.refresh()
        self.state = "Uncompleted"
        Order.register.update_state(self)
        
    def confirm(self):
        self.state = "Completed Successfully"
        Order.register.update_state(self)
        
    def destroy(self):
        self.user = None
        self.prod = None
        self.exist = False
        
    def make(self):
        self.prod.ordered()
        
    def data(self):

        return {
                "customer": self.user.id,
                "product": self.prod.bytes_to_str(),
                "State": self.state
                }

# simulates a simple payment card with balance and payment method.
class Card:
    register = CardRegistery()
    
    def __init__(self,owner, id, balance):
        
        self.id = id
        self.balance = balance
        self.owner = owner
        
        Card.register.register_card(self)
        
    def data(self):
        return {
                "user": self.owner,
                "balance": self.balance
                }
    
    def payment(self, amount):
        if self.balance < amount:
            return False
        
        self.balance -= amount
        Card.register.update_info(self)
        return True
        
# encodes username, email, password and card (if provided).
class User:
    numOfUsers = 0
    register = UserRegistery()

    def __init__(self, username, email = "", password = "", card = None):
        # key to encrypt/incrypt username using Fernet
        self.__SECRET_KEY = base64.urlsafe_b64decode(b'oJcU0eXALmageqxIiL0EBIBGK2UDVdjU3uvXTfX4HHc=')
        
        self.username = username
        
        self.id = self.encrypt_username()
        
        # check if the username already registered
        data = User.register.IsExist(self.id)
        
        # if it's registered fill data automatically
        if data:
            self.email = data["E-mail"]
            self.password = data["password"]
            self.orders = data["orders"]
            
            # in case of existing card linked, initialize the card object from card class
            if data["bank card"]:
                foundCard = User.register.find_card(data["bank card"])
                self.card_register(data["bank card"], foundCard["balance"])
                return

        
        else:
            # register user for the first time
            while email == "" or password == "":
                if email == "":
                    email = str(input("enter email:"))
                if password == "":
                    password = str(input("enter password: "))
            User.numOfUsers += 1
            
            self.email = email
            self.password = password
            self.orders = []
            
        if isinstance(card, int):
            
            while User.register.find_card(card):
                card = int(input("card already registered.\nEnter card: "))
            balance = float(input("enter balance: "))
            self.card_register(card, balance)
        else:
            self.card = None
            
        User.register.register_user(self)
        
        
    def encrypt_username(self):
        
        # AES in ECB mode is deterministic (same input → same output).
        cipher = Cipher(algorithms.AES(self.__SECRET_KEY), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad username to 16 bytes.
        data = self.username.encode()
        padder = padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()
        
        encrypted = encryptor.update(padded) + encryptor.finalize()
        
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_id(self): 
        
        cipher = Cipher(algorithms.AES(self.__SECRET_KEY), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        
        encrypted = base64.urlsafe_b64decode(self.id.encode())
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        
        # remove padding
        pad_len = decrypted[-1]
        
        return decrypted[:-pad_len].decode()
    
    def data(self):
        return {
                "UserName": self.username,
                "E-mail": self.email,
                "password": self.password,
                "bank card": self.card if self.card is None else self.card.id,
                "orders": self.orders
                }
    
    def card_register(self, id, balance):
        self.card = Card(self.id, id, balance)
        
    def make_order(self, prod):
        neworder = Order(self, prod)
        mes = "product unavailable for now."
        
        # exist is True when the product.available = True
        if neworder.exist:
            if not self.card:
                
                idcard = int(input("enter card: "))
                
                # if user enter card already registered by another user.
                while User.register.find_card(idcard):
                    print("card already registered.")
                    idcard = int(input("enter card: "))
                    
                balance = float(input("enter balance: "))
                
                # register the card in carts.json
                self.card_register(idcard, balance)
                
                # update the user card in users.json
                User.register.register_user(self)
                
            # unsuccessful payment -> cancel the order and mark as uncompeted
            if not self.card.payment(prod.price):
                mes = "card declined."
                neworder.cancel()
                User.register.register_user(self)
                
            # successful payement -> update state to successful
            else: 
                mes = "payment successful."
                neworder.confirm()
            
            # update the list of orders in users.json
            User.register.update_order(self, neworder.id)
            
        return mes

# holds product metadata and stock, provides ordering hooks
class Product:
    numOfProducts = 0
    register = ProductRegistery()
    
    def __init__(self, name, price = 0, stock = 0):
        
        data = Product.register.isExist(name)
        
        if data:
            data, id = data
            self.name = data["name"]
            self.price = data["price"]
            self.stock = data["stock"]
            self.available = data["availability"]
            self.id = self.str_to_bytes(id)

        else:
            Product.numOfProducts += 1
            self.name = name
            self.price = price
            self.stock = stock
            self.available = True
            # id in bytes
            self.id = uuid4().bytes
            
        self.refresh()
        
        Product.register.register_prod(self)
        
    def str_to_bytes(self, id_str: str) -> bytes:
        return base64.urlsafe_b64decode(id_str)
    
    def bytes_to_str(self) -> str:
        return base64.urlsafe_b64encode(self.id).decode() 
    
    #checks availablity of product
    def refresh(self):
        self.available = True if self.stock > 0 else False
        Product.register.update_prod(self)
    
    # called in make function of order class
    def ordered(self):
        self.stock -= 1
        self.refresh()
        
    def data(self):
        return {
                "name": self.name,
                "price": self.price,
                "stock": self.stock,
                "availability": self.available
                }
    

p1 = Product("iPhone 13", 3000, 5)
p2 = Product("macbook", 8000, 2)
p3 = Product("iPad", 5000, 10)
p4 = Product("alienware m15 r7", 20000, 1)

u1 = User("taha", "1@gmail.com", "392")
u2 = User("abdo", "2@gmail.com", "098",21)
u3 = User("marwan", "3@gmail.com", "567")
u4 = User("jihad",  "4@gmail.com", "irhabi")


print(u4.make_order(p3))