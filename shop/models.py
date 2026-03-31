from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Stock & Main Image
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=False)

    # Size Selection
    has_s = models.BooleanField(default=True, verbose_name="Small Available")
    has_m = models.BooleanField(default=True, verbose_name="Medium Available")
    has_l = models.BooleanField(default=True, verbose_name="Large Available")
    has_xl = models.BooleanField(default=False, verbose_name="XL Available")

    def __str__(self):
        return self.name

    # --- NAYA FUNCTION: Discount Percentage nikalne ke liye ---
    @property
    def get_discount_percentage(self):
        if self.discount_price and self.price > self.discount_price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return int(discount)
        return 0

    # --- NAYA FUNCTION: Stock Alert check karne ke liye ---
    @property
    def is_low_stock(self):
        return self.stock <= 5

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.name}"

# --- NAYA FEATURE: Product Colors (Ek product ke multiple colors ke liye) ---
class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color_name = models.CharField(max_length=50) # e.g. "Jet Black"
    color_code = models.CharField(max_length=7, help_text="Hex code e.g. #000000")

    def __str__(self):
        return f"{self.color_name} for {self.product.name}"

# --- FEATURE: Order Management with Auto-Stock Update ---
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    selected_size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            if self.product and self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

# --- NAYA FEATURE: Product Reviews (Feedback System) ---
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} for {self.product.name}"

# --- NAYA FEATURE: Home Page Slider (Bannners ke liye) ---
class HomeSlider(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='sliders/')
    link_url = models.CharField(max_length=500, default='/', help_text="Button kahan jaye?")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# ======================== NAYE FEATURES (AB ADD KIYE) ========================

# --- NAYA FEATURE: Newsletter (Marketing emails save karne ke liye) ---
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# --- NAYA FEATURE: Contact Message (Direct user contact ke liye) ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

# --- NAYA FEATURE: Brand Info (Phone, Social Links wagera change karne ke liye) ---
class BrandSetting(models.Model):
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, help_text="e.g. +923001234567")
    contact_email = models.EmailField()
    office_address = models.TextField()

    class Meta:
        verbose_name = "Brand Setting"
        verbose_name_plural = "Brand Settings"

    def __str__(self):
        return "Global Brand Settings"