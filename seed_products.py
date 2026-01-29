import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from marketra.models import Product

products = [
    {
        'name': 'Executive minimalist Desk',
        'category': 'Office',
        'price': 1299.00,
        'stock_status': 'In Stock',
        'ai_rank': 1,
        'is_featured': True
    },
    {
        'name': 'Precision Wireless Mouse',
        'category': 'Tech',
        'price': 89.00,
        'stock_status': 'Out of Stock',
        'ai_rank': 5,
        'is_featured': True
    },
    {
        'name': 'Smart Chronograph V2',
        'category': 'Wearables',
        'price': 450.00,
        'stock_status': 'Limited Edition',
        'ai_rank': 2,
        'is_featured': True
    },
    {
        'name': 'Leather Portfolio Case',
        'category': 'Essentials',
        'price': 210.00,
        'stock_status': 'In Stock',
        'ai_rank': 3,
        'is_featured': True
    },
    {
        'name': 'Ergonomic Chair Pro',
        'category': 'Office',
        'price': 850.00,
        'stock_status': 'In Stock',
        'ai_rank': 4,
        'is_featured': False
    },
    {
        'name': 'Noise Cancelling Headphones',
        'category': 'Tech',
        'price': 299.00,
        'stock_status': 'In Stock',
        'ai_rank': 6,
        'is_featured': False
    },
    {
        'name': 'Minimalist Table Lamp',
        'category': 'Home',
        'price': 120.00,
        'stock_status': 'In Stock',
        'ai_rank': 7,
        'is_featured': False
    },
    {
        'name': 'Mechanical Keyboard X',
        'category': 'Tech',
        'price': 180.00,
        'stock_status': 'In Stock',
        'ai_rank': 8,
        'is_featured': False
    },
    {
        'name': 'Premium Coffee Press',
        'category': 'Kitchen',
        'price': 75.00,
        'stock_status': 'In Stock',
        'ai_rank': 9,
        'is_featured': False
    },
    {
        'name': 'Aluminum Laptop Stand',
        'category': 'Tech',
        'price': 45.00,
        'stock_status': 'In Stock',
        'ai_rank': 10,
        'is_featured': False
    }
]

def populate():
    Product.objects.all().delete()
    for p_data in products:
        Product.objects.create(**p_data)
    print("Database populated with sample products.")

if __name__ == '__main__':
    populate()
