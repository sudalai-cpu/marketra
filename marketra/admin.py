from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_status', 'ai_rank', 'is_featured')
    list_filter = ('category', 'stock_status', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_status', 'is_featured', 'ai_rank')
