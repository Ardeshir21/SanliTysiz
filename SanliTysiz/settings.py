"""
Django settings for SanliTysiz project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# This part of code is for keep secret variables secure and also it to change some parameters for Development/Production
# It returns the secrets_dict which can be used in the main code
# This file is different in Server and my local PC
secret_file = 'SanliTysizKEYS.txt'
secrets = ['SECRET_KEY', 'DEBUG' , 'DATABASE_NAME', 'DATABASE_USERNAME', 'DATABASE_PASSWORD',
 'EMAIL_HOST', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD']
SECRETS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(SECRETS_DIR, secret_file)
secrets_dict = {}
with open(filepath) as fp:
   line = fp.readline()
   for item in secrets:
       secrets_dict[item] = line.strip()
       line = fp.readline()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets_dict['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# The DEBUG value in 'SanliTysizKEYS.txt' is an empty string ''
# I used bool() to return False
DEBUG = bool(secrets_dict['DEBUG'])

ALLOWED_HOSTS = ['161.35.103.31',
                 'localhost',
                 '127.0.0.1',
                 'www.sanli-tysiz.com.tr',
                 'sanli-tysiz.com.tr',
                 ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My applications
    'SanliTysiz.apps.baseApp',
    # for models Text editor
    'ckeditor',
    'ckeditor_uploader',
    # for models phone number field
    'phonenumber_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SanliTysiz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'SanliTysiz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Digital Ocean Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secrets_dict['DATABASE_NAME'],
        'USER': secrets_dict['DATABASE_USERNAME'],
        'PASSWORD': secrets_dict['DATABASE_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# This seeting is for scss files
# STATICFILES_FINDERS = ['django.contrib.staticfiles.finders.FileSystemFinder',
#                         'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#                         # other finders
#                         'compressor.finders.CompressorFinder',]
# COMPRESS_PRECOMPILERS = (
#     ('text/x-scss', 'django_libsass.SassCompiler'),
# )
# COMPRESS_OFFLINE = True
# LIBSASS_OUTPUT_STYLE = 'compressed'

STATIC_URL = '/static/'

# The root for collecting all static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# This is for production use only.
# https://docs.djangoproject.com/en/1.10/ref/contrib/staticfiles/#manifeststaticfilesstorage
if DEBUG == False:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# The root for uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# The root for uploaded files using CKeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_DATE = False

# CKeditor configurations
CKEDITOR_CONFIGS = {
    'default': {

        'skin': 'moono',
        # 'skin': 'office2013',



        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],


        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'Preview', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Replace']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']}
        ],

        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 300,
        'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        # "removePlugins": "iframe",
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}
