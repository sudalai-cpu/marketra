import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from marketra.models import Category, Product

# Create Category
office, _ = Category.objects.get_or_create(name='Office', slug='office', description='Premium workspace essentials')
lifestyle, _ = Category.objects.get_or_create(name='Lifestyle', slug='lifestyle', description='High-end luxury lifestyle products')

# Clear existing products
Product.objects.all().delete()

# Create Products
products = [
    {
        'name': 'Ergo-Pro Business Chair',
        'category': office,
        'price': 499.99,
        'description': 'The Ergo-Pro Business Chair is designed for ultimate comfort and productivity. Featuring breathable mesh, adjustable lumbar support, and a sleek minimalist design, it is the perfect addition to any modern office.',
        'stock_status': 'In Stock',
        'ai_rank': 1,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1505797149-43b00fe2e043?auto=format&fit=crop&q=80&w=800'
    },
    {
        'name': 'Minimalist Oak Desk',
        'category': office,
        'price': 899.00,
        'description': 'Handcrafted from solid oak, this minimalist desk offers a spacious work area and a clean aesthetic. Its timeless design ensures it remains a focal point of your workspace for years to come.',
        'stock_status': 'In Stock',
        'ai_rank': 2,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&q=80&w=800'
    },
    {
        'name': 'Ambient Studio Light',
        'category': lifestyle,
        'price': 129.50,
        'description': 'Create the perfect mood with the Ambient Studio Light. With adjustable brightness and color temperature, it provides soft, professional lighting for your workspace or home.',
        'stock_status': 'In Stock',
        'ai_rank': 3,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1534073828943-f801091bb18b?auto=format&fit=crop&q=80&w=800'
    },
    {
        'name': 'Smart Leather Briefcase',
        'category': lifestyle,
        'price': 345.00,
        'description': 'The Smart Leather Briefcase combines classic style with modern technology. Featuring premium Italian leather and a dedicated laptop sleeve, it is the essential companion for the professional on the move.',
        'stock_status': 'Out of Stock',
        'ai_rank': 4,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1547949003-9792a18a2601?auto=format&fit=crop&q=80&w=800'
    }
]

for p_data in products:
    Product.objects.create(**p_data)

print(f"Successfully created {len(products)} products.")
