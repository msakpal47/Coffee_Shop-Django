import os
import django
import re

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

from coffee_Shop.models import MenuItem

# Regex to match emojis and special characters (keeping basic punctuation if needed, but removing icons)
# This simple regex removes non-ascii characters which covers most emojis.
# Adjust if you want to keep some specific non-ascii chars.
def clean_name(name):
    # Remove emojis and other symbols (anything not alphanumeric, space, or basic punctuation)
    # This regex [^\w\s,\.\-\(\)\/] might be too aggressive or too loose depending on exact needs.
    # But for "☕ Hot Coffee", removing non-ascii is a good start or just stripping specific ones.
    
    # Strategy 1: Remove common emoji ranges (simplest for this request)
    # Strategy 2: Keep only allowed characters (A-Z, a-z, 0-9, space, specific punctuation)
    
    # Let's go with Strategy 2: Keep alphanumeric and basic punctuation
    cleaned = re.sub(r'[^\w\s\-\(\)\/\.,&]', '', name).strip()
    return cleaned

items = MenuItem.objects.all()
print("Cleaning item names...")
for item in items:
    original_name = item.name
    cleaned_name = clean_name(original_name)
    
    if original_name != cleaned_name:
        print(f"Renaming: '{original_name}' -> '{cleaned_name}'")
        item.name = cleaned_name
        item.save()
    else:
        # print(f"Skipping: '{original_name}' (already clean)")
        pass

print("Done.")
