"""
Django settings for the paleoanthro project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import local_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = local_settings.STATIC_URL  # import from local_settings.py
STATIC_ROOT = local_settings.STATIC_ROOT  # development

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = local_settings.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = local_settings.MEDIA_URL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS

POSTGIS_VERSION = (2, 0, 1)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Django Fiber Apps
    'django.contrib.staticfiles',
    'mptt',
    'compressor',
    'easy_thumbnails',
    'fiber',

    # Additional 3rd party apps
    'ckeditor',
    'captcha',

    # Project Apps
    'home',  # main site app
    'meetings',  # meetings app
    'journal',  # paleoanthro journal app
    'dissertations',  # dissertation app
    'members',  # membership app
)

# These entries extended by entries below in Django Fiber section
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'paleoanthro.urls'

WSGI_APPLICATION = 'paleoanthro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # Sqlite database backend
        'NAME': os.path.join(BASE_DIR, 'paleoanthro.sqlite'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True





##############################
## Django ckeditor Settings ##
##############################
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"


###########################
## Django Fiber Settings ##
###########################
import django.conf.global_settings as DEFAULT_SETTINGS

# Overides Middleware Classes defined above
MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES + (
    'fiber.middleware.ObfuscateEmailAddressMiddleware',
    'fiber.middleware.AdminPageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)


"""
Added to appropriate section above
INSTALLED_APPS = (
    ...
    'django.contrib.staticfiles',
    'mptt',
    'compressor',
    'easy_thumbnails',
    'fiber',
    ...
)
"""

# import os  # Already imported above
# BASE_DIR = os.path.abspath(os.path.dirname(__file__)) # Already defined above

# STATIC_URL = '/static/' # Already defined above
STATICFILES_FINDERS = DEFAULT_SETTINGS.STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_NOISE_FUNCTIONS = []

#######################
# email configuration #
#######################
EMAIL_HOST = local_settings.EMAIL_HOST
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = local_settings.DEFAULT_FROM_EMAIL
SERVER_EMAIL = local_settings.SERVER_EMAIL