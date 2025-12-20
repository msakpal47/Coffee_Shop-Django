import os
import django
from django.core.files import File
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

from coffee_Shop.models import MenuItem

# Source directory for images
SOURCE_IMG_DIR = os.path.join(os.getcwd(), 'frontend', 'Items')

items_data = [
    # ☕ Hot Coffee
    {
        "name": "Filter Coffee",
        "description": "Traditional South Indian filter coffee with strong decoction and frothy milk.",
        "price": "60",
        "image_filename": "filter_coffe.jpg"
    },
    {
        "name": "Masala Coffee",
        "description": "Coffee brewed with Indian spices like cardamom and cinnamon.",
        "price": "80",
        "image_filename": "Masala Coffee.jpg"
    },
    {
        "name": "Cappuccino",
        "description": "Rich espresso topped with thick milk foam.",
        "price": "120",
        "image_filename": "Cappuccino.jpg"
    },
    {
        "name": "Latte",
        "description": "Smooth espresso with steamed milk.",
        "price": "130",
        "image_filename": "Latte.jpg"
    },
    {
        "name": "Espresso",
        "description": "Strong and bold single-shot coffee.",
        "price": "90",
        "image_filename": "Espresso.jpg"
    },
    # 🧊 Cold Coffee
    {
        "name": "Cold Coffee",
        "description": "Chilled coffee blended with milk and sugar.",
        "price": "140",
        "image_filename": "Cold Coffee.jpg"
    },
    {
        "name": "Cold Coffee with Ice Cream",
        "description": "Cold coffee topped with vanilla ice cream.",
        "price": "160",
        "image_filename": "Cold Coffee with Ice Cream.jpg"
    },
    {
        "name": "Chocolate Cold Coffee",
        "description": "Coffee blended with chocolate syrup.",
        "price": "170",
        "image_filename": "Chocolate Cold Coffee.jpg"
    },
    {
        "name": "Mocha",
        "description": "Espresso mixed with chocolate and milk.",
        "price": "150",
        "image_filename": "Mocha.jpg"
    },
    # 🍵 Tea (Indian Style)
    {
        "name": "Masala Chai",
        "description": "Indian tea brewed with spices and milk.",
        "price": "40",
        "image_filename": "Masala Chai ad.jpg"
    },
    {
        "name": "Ginger Tea",
        "description": "Hot tea infused with fresh ginger.",
        "price": "45",
        "image_filename": "Ginger Tea.jpg"
    },
    {
        "name": "Elaichi Tea",
        "description": "Tea flavored with cardamom.",
        "price": "45",
        "image_filename": "Elaichi Tea.jpg"
    },
    # 🥐 Snacks & Bakery
    {
        "name": "Veg Puff",
        "description": "Crispy puff pastry filled with spicy vegetables.",
        "price": "50",
        "image_filename": "Veg Puff.jpg"
    },
    {
        "name": "Paneer Puff",
        "description": "Puff pastry stuffed with spicy paneer.",
        "price": "60",
        "image_filename": "Paneer Puff.jpg"
    },
    {
        "name": "Butter Croissant",
        "description": "Soft and flaky butter croissant.",
        "price": "90",
        "image_filename": "Butter Croissant.jpg"
    },
    {
        "name": "Chocolate Muffin",
        "description": "Moist muffin loaded with chocolate chips.",
        "price": "80",
        "image_filename": "Chocolate Muffin.jpg"
    },
    {
        "name": "Veg Sandwich",
        "description": "Fresh vegetables layered with butter and spices.",
        "price": "70",
        "image_filename": "Veg Sandwich.jpg"
    },
    # 🍰 Desserts
    {
        "name": "Chocolate Brownie",
        "description": "Rich chocolate brownie served warm.",
        "price": "120",
        "image_filename": "Chocolate Brownie.jpg"
    },
    {
        "name": "Cheesecake",
        "description": "Creamy cheesecake with biscuit base.",
        "price": "160",
        "image_filename": "Cheesecake.jpg"
    },
    {
        "name": "Coffee Cake",
        "description": "Soft sponge cake infused with coffee flavor.",
        "price": "110",
        "image_filename": "Coffee Cake.jpg"
    },
    # 🥤 Extras
    {
        "name": "Hot Chocolate",
        "description": "Thick hot chocolate made with cocoa and milk.",
        "price": "140",
        "image_filename": "Hot Chocolate.jpg"
    },
    {
        "name": "Milkshake (Vanilla/Chocolate/Strawberry)",
        "description": "Thick and creamy milkshake.",
        "price": "150",
        "image_filename": "Milkshake Vanilla Chocolate Strawberry.jpg"
    }
]

for item_data in items_data:
    name = item_data['name']
    if MenuItem.objects.filter(name=name).exists():
        print(f"Item '{name}' already exists. Skipping.")
        continue
    
    print(f"Adding '{name}'...")
    menu_item = MenuItem(
        name=name,
        description=item_data['description'],
        price=Decimal(item_data['price'])
    )
    
    image_path = os.path.join(SOURCE_IMG_DIR, item_data['image_filename'])
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            menu_item.image.save(item_data['image_filename'], File(f), save=True)
            print(f"  - Image saved: {item_data['image_filename']}")
    else:
        print(f"  - WARNING: Image not found at {image_path}")
        menu_item.save()

print("Done.")
