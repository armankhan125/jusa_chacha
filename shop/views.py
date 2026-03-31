from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Product, Category, Order, Review, ProductImage, 
    HomeSlider, Newsletter, ContactMessage, BrandSetting
)
from django.contrib import messages
import urllib.parse

# --- 1. ADMIN STATS (Waisa hi hai) ---
def admin_dashboard_stats(request):
    return {
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status='Pending').count(),
        "total_products": Product.objects.count(),
        "total_reviews": Review.objects.count(),
    }

# --- 2. PRODUCT LIST (Aapka logic + Sirf Sliders fetch kiye) ---
def product_list(request):
    categories = Category.objects.all() 
    sliders = HomeSlider.objects.filter(is_active=True) # Naya data
    
    query = request.GET.get('search')
    cat_id = request.GET.get('category')
    sort_option = request.GET.get('sort')
    
    products = Product.objects.all()

    if cat_id:
        products = products.filter(category_id=cat_id)
    if query:
        products = products.filter(name__icontains=query)

    if sort_option == 'low':
        products = products.order_by('price')
    elif sort_option == 'high':
        products = products.order_by('-price')
    else:
        products = products.order_by('-is_featured', '-id')

    return render(request, 'shop/index.html', {
        'products': products, 
        'categories': categories,
        'sliders': sliders, # Sirf list mein add kiya
        'current_category': cat_id,
        'current_sort': sort_option
    })

# --- 3. PRODUCT DETAIL (Aapka original logic 100% same) ---
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    gallery = product.images.all() 
    colors = product.colors.all() # Naya data
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    if request.method == 'POST':
        if 'order_submit' in request.POST:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            size = request.POST.get('size')
            qty_raw = request.POST.get('qty', 1)
            
            if not name or not phone or not address or not size:
                messages.error(request, "Please select size and fill all details!")
                return redirect('product_detail', pk=product.pk)

            try:
                qty = int(qty_raw)
            except ValueError:
                qty = 1
            
            current_price = product.discount_price if product.discount_price else product.price
            total = current_price * qty
            
            new_order = Order.objects.create(
                product=product,
                customer_name=name,
                customer_phone=phone,
                customer_address=address,
                selected_size=size,
                quantity=qty,
                total_price=total,
                status='Pending'
            )
            
            whatsapp_msg = (
                f"🚀 *NEW ORDER: #{new_order.id}*\n"
                f"--------------------------\n"
                f"📦 *Item:* {product.name}\n"
                f"📏 *Size:* {size}\n"
                f"🔢 *Qty:* {qty}\n"
                f"💰 *Total:* RS. {total}\n"
                f"--------------------------\n"
                f"👤 *Customer:* {name}\n"
                f"📞 *Phone:* {phone}\n"
                f"📍 *Address:* {address}\n"
                f"--------------------------\n"
                f"Sent from JUSA & CHACHA Web"
            )
            
            encoded_msg = urllib.parse.quote(whatsapp_msg)
            # Aapka number waisa hi rakha hai
            whatsapp_url = f"https://wa.me/923105631656?text={encoded_msg}"
            return redirect(whatsapp_url)

        elif 'review_submit' in request.POST: 
            rev_name = request.POST.get('rev_name')
            rev_rating = request.POST.get('rev_rating')
            rev_comment = request.POST.get('rev_comment')
            
            if rev_name and rev_comment:
                Review.objects.create(
                    product=product,
                    name=rev_name,
                    rating=rev_rating,
                    comment=rev_comment
                )
                messages.success(request, "Thank you for your review!")
            return redirect('product_detail', pk=product.pk)

    return render(request, 'shop/detail.html', {
        'product': product,
        'gallery': gallery,
        'colors': colors, # Sirf extra add kiya
        'reviews': reviews,
        'related_products': related_products 
    })

# --- 4. ABOUT (Waisa hi hai) ---
def about(request):
    return render(request, 'shop/about.html')

# --- 5. NAYA FUNCTION (Alag se newsletter ke liye) ---
def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
            messages.success(request, "Subscribed successfully!")
    return redirect(request.META.get('HTTP_REFERER', '/'))