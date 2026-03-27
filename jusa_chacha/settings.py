import os
from pathlib import Path

# --- BASE DIRECTORY ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SERVER & SECURITY SETTINGS ---
SECRET_KEY = 'django-insecure-apki-purani-key-yahan-honi-chahiye'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
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

# --- JAZZMIN SETTINGS (Optimized for Visibility) ---
JAZZMIN_SETTINGS = {
    "site_title": "Jusa & Chacha Admin",
    "site_header": "JUSA & CHACHA",
    "site_brand": "JUSA & CHACHA",
    
    # Force Top Menu and User Menu
    "show_topmenu": True,
    "show_ui_builder": False,
    
    "usermenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
        {"name": "WhatsApp Help", "url": "https://wa.me/923105631656", "new_window": True},
    ],

    "topmenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
        {"model": "shop.Order"},
    ],

    "welcome_sign": "Welcome to Jusa & Chacha Control Panel",
    "copyright": "Jusa & Chacha Ltd",
    "search_model": ["shop.Product", "shop.Order"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["shop.Order", "shop.Product", "shop.Category", "shop.Review"],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "shop.Product": "fas fa-tshirt",
        "shop.Order": "fas fa-shopping-cart",
        "shop.Category": "fas fa-list",
        "shop.Review": "fas fa-star",
        "shop.View Sales Report": "fas fa-chart-line",
        "shop.Go to Website": "fas fa-external-link-alt", # Sidebar icon
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

# --- UI TWEAKS ---
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False, # Changed to False to prevent hiding
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