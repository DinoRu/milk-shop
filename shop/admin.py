from django.contrib import admin
from .models import Product, Customer, Cart, Payment, Order, OrderItem, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discount_price', 'category', 'prod_image']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'locality', 'city', 'number', 'zipcode', 'state']
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'quantity']
"""
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount']
"""
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ['id', 'customer','created', 'update', 'status', 'paid']
    inlines = [OrderItemInline]

@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
