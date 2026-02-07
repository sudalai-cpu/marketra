import os
import django
import random
from django.utils.text import slugify

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from marketra.models import Product, Category

def populate():
    print("Starting database population...")

    # Define Categories and Products
    data = {
        'Mobile': [
            'iPhone 15 Pro Max', 'Samsung Galaxy S24 Ultra', 'Google Pixel 8 Pro', 'OnePlus 12', 
            'Xiaomi 14 Ultra', 'Sony Xperia 1 V', 'Motorola Edge 50 Pro', 'Asus ROG Phone 8', 
            'Huawei Pura 70', 'Nothing Phone 2'
        ],
        'Clothing': [
            'Classic White T-Shirt', 'Skinny Fit Denim Jeans', 'Casual Hooded Sweatshirt', 
            'Formal Business Suit', 'Summer Floral Dress', 'Leather Biker Jacket', 
            'Athletic Running Shorts', 'Woolen Winter Coat', 'Striped Polo Shirt', 
            'Cotton Chino Pants'
        ],
        'Home Decor': [
            'Modern Abstract Vase', 'Velvet Throw Pillow', 'Minimalist Wall Clock', 
            'Ceramic Table Lamp', 'Handwoven Area Rug', 'Wooden Picture Frame', 
            'Scented Soy Candle', 'Decorative Wall Mirror', 'Artificial Potted Plant', 
            'Geometric Bookshelf'
        ],
        'Fitness': [
            'Adjustable Dumbbell Set', 'Yoga Mat Extra Thick', 'Resistance Bands Loop', 
            'Kettlebell 10kg', 'Foam Roller for Recovery', 'Jump Rope Speed Rope', 
            'Exercise Ball 65cm', 'Push Up Bars Stands', 'Ab Roller Wheel Kit', 
            'Running Armband Phone Holder'
        ],
        'Books': [
            'The Great Gatsby', 'To Kill a Mockingbird', '1984 by George Orwell', 
            'Pride and Prejudice', 'The Catcher in the Rye', 'The Hobbit', 
            'Harry Potter Unit', 'The Alchemist', 'The Da Vinci Code', 
            'The Lord of the Rings'
        ]
    }

    total_created = 0

    for category_name, product_names in data.items():
        # Create Category
        slug = slugify(category_name)
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': slug, 'description': f'All kinds of {category_name} products.'}
        )
        if created:
            print(f"Created Category: {category_name}")
        else:
            print(f"Existing Category: {category_name}")

        # Create Products
        for prod_name in product_names:
            # Check if product exists to avoid duplicates if re-run
            if not Product.objects.filter(name=prod_name).exists():
                price = random.randint(500, 10000)
                description = f"This is a high-quality {prod_name} designed for the modern user."
                
                Product.objects.create(
                    name=prod_name,
                    category=category,
                    price=price,
                    description=description,
                    image='products/default.jpg',
                    stock_status='In Stock',
                    ai_rank=random.randint(1, 100),
                    is_featured=(random.random() > 0.8) # 20% chance of being featured
                )
                total_created += 1
            else:
                print(f"  Skipped duplicate: {prod_name}")

    print(f"\nSuccess! Added {total_created} new products across {len(data)} categories.")

if __name__ == '__main__':
    populate()
