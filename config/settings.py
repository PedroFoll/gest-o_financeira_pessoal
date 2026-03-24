"""
Configurações do projeto Django.
Usa python-decouple para carregar variáveis do arquivo .env
"""
from pathlib import Path
from decouple import config, Csv

# =============================================================
# PATHS
# =============================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================
# SEGURANÇA
# =============================================================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# =============================================================
# APPS INSTALADOS
# =============================================================
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # adicione bibliotecas de terceiros aqui
]

LOCAL_APPS = [
    # páginas do projeto — adicione cada pages.<nome> aqui
    'pages.home',
    'pages.usuarios',
    'pages.categorias',
    'pages.lancamentos',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# =============================================================
# MIDDLEWARE
# =============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # servir static em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =============================================================
# URLs
# =============================================================
ROOT_URLCONF = 'config.urls'


# =============================================================
# TEMPLATES
# =============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # templates globais: templates/base.html, templates/partials/
        'DIRS': [BASE_DIR / 'templates'],
        # APP_DIRS=True: Django encontra templates/ dentro de cada app/página
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


# =============================================================
# WSGI / ASGI
# =============================================================
WSGI_APPLICATION = 'config.wsgi.application'


# =============================================================
# BANCO DE DADOS — SQLite com WAL mode
# =============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'init_command': 'PRAGMA journal_mode=WAL;',
        },
    }
}


# =============================================================
# AUTENTICAÇÃO — VALIDAÇÃO DE SENHA
# =============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================
# INTERNACIONALIZAÇÃO
# =============================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# =============================================================
# ARQUIVOS ESTÁTICOS (CSS, JS, imagens)
# =============================================================
STATIC_URL = '/static/'

# Auto-descobre pastas static/ de cada componente em templates/partials/
import os as _os

def _discover_component_statics(templates_dir):
    """Retorna lista de pastas static/ dentro de cada componente em partials/."""
    partials_dir = templates_dir / 'partials'
    if not partials_dir.exists():
        return []
    return [
        partials_dir / component / 'static'
        for component in _os.listdir(partials_dir)
        if (partials_dir / component / 'static').is_dir()
    ]

# Pastas onde o Django procura arquivos estáticos no desenvolvimento
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    *_discover_component_statics(BASE_DIR / 'templates'),
]

# Destino do `collectstatic` (produção)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise comprime e faz cache dos arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =============================================================
# ARQUIVOS DE MÍDIA (uploads do usuário)
# =============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================
# CAMPO PADRÃO PARA CHAVES PRIMÁRIAS
# =============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================
# REDIRECIONAMENTOS DE AUTENTICAÇÃO
# =============================================================
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# =============================================================
# MENSAGENS — mapeamento para classes CSS Bootstrap
# =============================================================
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG:   'secondary',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR:   'danger',
}


# =============================================================
# SEGURANÇA EXTRA EM PRODUÇÃO (ativo somente quando DEBUG=False)
# =============================================================
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
