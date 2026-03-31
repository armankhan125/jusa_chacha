from django.contrib import admin
from .models import Product, Category, ProductImage, Order, Review, HomeSlider, ProductColor, Newsletter
from django.db.models import Sum

# --- Product Colors (Inline) ---
class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 2
    fields = ['color_name', 'color_code']

# --- Gallery images (Product Inline) ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 
    fields = ['image']

# --- Category Management ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

# --- Product Management ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    # Ab Gallery aur Colors dono aik hi page par nazar ayenge
    inlines = [ProductImageInline, ProductColorInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description', 'image', 'is_featured')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Available Sizes', {
            'fields': ('has_s', 'has_m', 'has_l', 'has_xl'),
            'description': 'Tick those sizes which are currently in stock.'
        }),
    )

# --- Home Page Slider Management ---
@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)

# --- Newsletter Management ---
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

# --- Detailed Order Management with Stats ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'product', 'selected_size', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'product')
    search_fields = ('customer_name', 'customer_phone', 'customer_address')
    list_editable = ('status',) 
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'customer_phone', 'customer_address')
        }),
        ('Order Details', {
            'fields': ('product', 'selected_size', 'quantity', 'total_price', 'status', 'created_at')
        }),
    )

    def changelist_view(self, request, extra_context=None):
        total_orders = Order.objects.count()
        # "Delivered" ya "Confirmed" status ke mutabiq sales calculate karein
        total_sales = Order.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
        pending_orders = Order.objects.filter(status='Pending').count()

        extra_context = extra_context or {}
        extra_context['show_widgets'] = True 
        extra_context['total_orders'] = total_orders
        extra_context['total_sales'] = f"Rs. {total_sales}"
        extra_context['pending_orders'] = pending_orders
        
        return super().changelist_view(request, extra_context=extra_context)

# --- Review Management ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comment', 'product__name')