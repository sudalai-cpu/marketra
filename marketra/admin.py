from django.contrib import admin
from .models import Category, Product, ViewHistory, Section

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'display_order', 'slug')
    list_editable = ('display_order',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_status', 'ai_rank', 'is_featured')
    list_filter = ('category', 'stock_status', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_status', 'is_featured', 'ai_rank')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'icon')
    list_editable = ('display_order', 'icon')


admin.site.register(ViewHistory)
