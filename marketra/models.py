from django.db import migrations, models
from django.contrib.auth.models import User

class Section(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='sections/', blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True, help_text="Fallback icon URL")

    def __str__(self):
        return self.name

class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    stock_status = models.CharField(max_length=50, default='In Stock')
    ai_rank = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Static URL fallback
    image_url = models.URLField(blank=True, null=True)
    # Dynamic Image upload
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100, help_text="Full name for delivery")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.street_address}"

    class Meta:
        verbose_name_plural = "Addresses"

class StyleProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='style_profile')
    # Using JSONField for flexibility with AI data points
    style_keywords = models.JSONField(default=list, blank=True, help_text="List of AI-derived style keywords")
    sizes = models.JSONField(default=dict, blank=True, help_text="User sizes (e.g., {'top': 'M', 'shoe': '10'})")
    favorite_colors = models.CharField(max_length=255, blank=True)
    fashion_goals = models.TextField(blank=True, help_text="User's description of their style goals")

    def __str__(self):
        return f"Style Profile for {self.user.username}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlisted_by', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class Collection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='collection')
    products = models.ManyToManyField(Product, related_name='collected_by', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collection for {self.user.username}"

class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # AI-kku intha foreign key romba mukkiyam
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) 
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    
    # Advanced AI Logic-kaka intha rendu field extra:
    interaction_type = models.CharField(max_length=20, default='view') # 'view', 'wishlist', 'buy'
    strength = models.IntegerField(default=1) # View=1, Wishlist=3, Buy=5
    
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.product_name}"