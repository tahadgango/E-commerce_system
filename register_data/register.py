from pathlib import Path
from json import load, dump

general = Path("c:/Users/jabar/OneDrive/Desktop/project/e-commerce/register_data/data")
misData = Path("c:/Users/jabar/OneDrive/Desktop/project/e-commerce/register_data/missing")
idsPath = Path("c:/Users/jabar/OneDrive/Desktop/project/e-commerce/register_data/ids")

class Registery:
    filename = misData / "default.json"
   
    def __init__(self):
        super().__init__()
        self.filename = Registery.filename

    def load(self, file):
        with open(file, "r") as f:
            return load(f)
        
    def save(self, newDict, file):
        with open(file, "w") as f:
            dump(newDict, f, indent=4)

class CardRegistery(Registery):
    filename = general / "carts.json"
    
    def __init__(self):
        super().__init__()
        self.filename = CardRegistery.filename
    
    def register_card(self, card):
        cardDict = self.load(self.filename)
        cardDict[str(card.id)] = card.data()
        self.save(cardDict, self.filename)
        
    def update_info(self, card):
        cardDict = self.load(self.filename)
        cardDict[str(card.id)]["balance"] = card.balance
        self.save(cardDict, self.filename)
        
    def find(self, id):
        cardDict = self.load(self.filename)
        id = str(id)
        return cardDict[id] if id in cardDict else False
        
class UserRegistery(Registery):
    filename = general / "users.json"
    card_register = CardRegistery()
    
    def __init__(self):
        super().__init__()
        self.filename = UserRegistery.filename
        
    def register_user(self, user):
        userDict = self.load(self.filename)
        userDict[user.id] = user.data()
        self.save(userDict, self.filename)
    
    def update_order(self, user, id):
        userDict = self.load(self.filename)
        userDict[user.id]["orders"].append(id)
        self.save(userDict, self.filename)
    
    def find_card(self, id):
        cardInfo = UserRegistery.card_register.find(id)
        return cardInfo

    def IsExist(self, id):
        userDict = self.load(self.filename)
        return userDict[id] if id in userDict else False
        
class ProductRegistery(Registery):
    prodFile = general / "products.json"
    idsFile = idsPath / "prodIds.json"
    
    def __init__(self):
        super().__init__()
        self.filename = ProductRegistery.prodFile
        self.idsFile = ProductRegistery.idsFile
        
    def register_prod(self, prod):
        prodDict = self.load(self.filename)
        prodDict[prod.bytes_to_str()] = prod.data()
        self.save(prodDict, self.filename)

        products = self.load(self.idsFile)
        products[prod.name] = prod.bytes_to_str()
        self.save(products, self.idsFile)
        
    def update_prod(self, prod):
        prodDict = self.load(self.filename)
        prodDict[prod.bytes_to_str()] = prod.data()
        self.save(prodDict, self.filename)

    def isExist(self, name):
        idDict = self.load(self.idsFile)
        
        if name not in idDict:
            return False
        
        prodDict = self.load(self.filename)  
        return (prodDict[idDict[name]], idDict[name])
        
class OrderRegistery(Registery):
    filename = general / "orders.json"
    idsFile = idsPath / "orderIds.json"
    
    def __init__(self):
        super().__init__()
        self.filename = OrderRegistery.filename
        self.idsFile = OrderRegistery.idsFile
    
    def register_order(self, order):
        orderDict = self.load(self.filename)
        id = len(orderDict) + 1
        orderDict[str(id)] = order.data()
        self.save(orderDict, self.filename)

        identifyOrder = self.load(self.idsFile)
        identifyOrder[str([order.user.id, order.prod.bytes_to_str()])] = id
        self.save(identifyOrder, self.idsFile)
        
        return id
