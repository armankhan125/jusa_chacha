from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"  # <--- Ye 'Categorys' ki spelling theek karega

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

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.product.name}"

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

    # Logic: Order save hote hi stock khud kam ho jaye
    def save(self, *args, **kwargs):
        if not self.pk: # Agar naya order hai
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