from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, Review, ProductImage
from django.contrib import messages
import urllib.parse

# --- NAYA: Admin Dashboard ke liye Stats ---
def admin_dashboard_stats(request):
    """Ye function Jazzmin dashboard par stats dikhaye ga"""
    return {
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status='Pending').count(),
        "total_products": Product.objects.count(),
        "total_reviews": Review.objects.count(),
    }

def product_list(request):
    categories = Category.objects.all() 
    query = request.GET.get('search')
    cat_id = request.GET.get('category')
    sort_option = request.GET.get('sort')
    
    # Base Queryset
    products = Product.objects.all()

    if cat_id:
        products = products.filter(category_id=cat_id)
        
    if query:
        products = products.filter(name__icontains=query)

    # Sorting Logic
    if sort_option == 'low':
        products = products.order_by('price')
    elif sort_option == 'high':
        products = products.order_by('-price')
    else:
        # Featured products top par, phir newest
        products = products.order_by('-is_featured', '-id')

    return render(request, 'shop/index.html', {
        'products': products, 
        'categories': categories,
        'current_category': cat_id,
        'current_sort': sort_option
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Hamari gallery 'images' related_name use karti hai
    gallery = product.images.all() 
    reviews = product.reviews.all().order_by('-created_at')
    
    # Related Products (Same category, excluding current product)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    if request.method == 'POST':
        # --- ORDER FORM LOGIC ---
        if 'order_submit' in request.POST:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            size = request.POST.get('size')
            qty_raw = request.POST.get('qty', 1)
            
            # Basic validation
            if not name or not phone or not address or not size:
                messages.error(request, "Please select size and fill all details!")
                return redirect('product_detail', pk=product.pk)

            try:
                qty = int(qty_raw)
            except ValueError:
                qty = 1
            
            current_price = product.discount_price if product.discount_price else product.price
            total = current_price * qty
            
            # Database mein order save karna
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
            
            # WhatsApp Message Formatting (Aapke Number ke sath)
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
            # Aapka real number 923105631656 check kar liya hai maine
            whatsapp_url = f"https://wa.me/923105631656?text={encoded_msg}"
            return redirect(whatsapp_url)

        # --- REVIEW FORM LOGIC ---
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
        'reviews': reviews,
        'related_products': related_products 
    })

def about(request):
    """About Us and Size Guide Page"""
    return render(request, 'shop/about.html')