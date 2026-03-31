import os
from pathlib import Path

# --- BASE DIRECTORY ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SERVER & SECURITY SETTINGS ---
SECRET_KEY = 'django-insecure-apki-purani-key-yahan-honi-chahiye'
DEBUG = True
# Purani line:
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'armankhan125.pythonanywhere.com']

# Nayi sahi line (Dono domains dal dein taake masla na ho):
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    'jusaandchacha.pythonanywhere.com', 
    'armankhan125.pythonanywhere.com'
]
ROOT_URLCONF = 'jusa_chacha.urls'

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'jazzmin',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- DATABASE SETTINGS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- STATIC & MEDIA FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- JAZZMIN SETTINGS (Mobile & UI Optimized) ---
JAZZMIN_SETTINGS = {
    "site_title": "Jusa & Chacha Admin",
    "site_header": "JUSA & CHACHA",
    "site_brand": "JUSA & CHACHA",
    
    # MOBILE FIX: Ye mobile par top menu enable karta hai
    "show_topmenu": True,
    "show_ui_builder": False,
    
    "usermenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
        {"name": "WhatsApp Help", "url": "https://wa.me/923105631656", "new_window": True},
    ],

    "topmenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
        {"model": "shop.Order"},
        {"model": "shop.Product"}, # Taake direct product pe ja sakein
    ],

    "welcome_sign": "Welcome to Jusa & Chacha Control Panel",
    "copyright": "Jusa & Chacha Ltd",
    "search_model": ["shop.Product", "shop.Order"],
    
    # MOBILE VIEW OPTIMIZATION
    "show_sidebar": True,
    "navigation_expanded": True, # Mobile par menu hamesha available rahega
    
    "order_with_respect_to": ["shop.Order", "shop.Product", "shop.Category", "shop.Review"],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "shop.Product": "fas fa-tshirt",
        "shop.Order": "fas fa-shopping-cart",
        "shop.Category": "fas fa-list",
        "shop.Review": "fas fa-star",
        "shop.View Sales Report": "fas fa-chart-line",
        "shop.Go to Website": "fas fa-external-link-alt",
    },
    
    "custom_links": {
        "shop": [
            {
                "name": "Go to Website", 
                "url": "/", 
                "icon": "fas fa-external-link-alt",
            },
            {
                "name": "View Sales Report", 
                "url": "admin:shop_order_changelist", 
                "icon": "fas fa-chart-line",
            }
        ]
    },
    
    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
}

# --- UI TWEAKS (For Better Mobile View) ---
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False, # Isse False rakha hai taake mobile par screen cover na ho
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "theme": "flatly", 
    "button_classes": {
        "primary": "btn-primary", "secondary": "btn-secondary",
        "info": "btn-info", "warning": "btn-warning",
        "danger": "btn-danger", "success": "btn-success"
    }
}

# --- NAYA: LOGIN/LOGOUT REDIRECTS ---
# Ye user ko login ya signup ke baad seedha home page par bhej denge
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'