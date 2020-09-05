from django.contrib import admin
from django import forms
from django.db import models
from .models import (Product_Category,
                    Product,
                    ProductImages)

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    list_display = ['product', 'image', 'display_order']
    list_editable = ['display_order']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    # other Inlines
    inlines = [
        ProductImagesInline,
    ]

    # Using Widgets
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple(attrs={'multiple': True})},
    }

class Product_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Category, Product_CategoryAdmin)
