from pathlib import Path
from json import dump
from cryptography.fernet import Fernet

general = Path("c:/Users/jabar/OneDrive/Desktop/project/e-commerce/register_data/data")
general.mkdir(parents=True, exist_ok=True)

idsPath = Path("c:/Users/jabar/OneDrive/Desktop/project/e-commerce/register_data/ids")
idsPath.mkdir(parents=True, exist_ok=True)

misData = Path("c:/Users/jabar/OneDrive/Desktop/project/e-commerce/register_data/missing")
misData.mkdir(parents=True, exist_ok=True)


dump({}, open(misData / "default.json", "w"), indent=4)
    
dump({}, open(general / "users.json", "w"), indent=4)
dump({}, open(general / "products.json", "w"), indent=4)
dump({}, open(general / "orders.json", "w"), indent=4)
dump({}, open(general / "carts.json", "w"), indent=4)
    
dump({}, open(idsPath / "prodIds.json", "w"), indent=4)
dump({}, open(idsPath / "orderIds.json", "w"), indent=4)


Skey = Fernet.generate_key()
