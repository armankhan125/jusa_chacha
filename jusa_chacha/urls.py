from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Views import ho rahe hain
from shop.views import product_list, product_detail, about 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home Page: Saare products nazar aayenge
    path('', product_list, name='product_list'),
    
    # Product detail page: Jab koi kisi shirt par click karega
    path('product/<int:pk>/', product_detail, name='product_detail'), 
    
    # About Us aur Size Guide page
    path('about/', about, name='about'), 
    
]

# Media aur Static files ki setting (Images aur CSS ke liye)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)