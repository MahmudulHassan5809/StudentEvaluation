import os
from django.contrib.messages import constants as messages


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7ggw!33w4ycon^*cl(+m(u1v78c@fzcc7l9sve@3$*s48r^!lu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Security Features
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")
# SECURE_CONTENT_TYPE_NOSNIFF = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'ALLOW'
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# SECURE_HSTS_PRELOAD = True


# Application definition

INSTALLED_APPS = [
    'accounts',
    'session',
    'programs',
    'course',
    'boards',
    'pages',
    'quizes',

    'baton',
    'django.contrib.admin',
    #'baton.autodiscover',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'crispy_forms',
    'django_cleanup',
    'widget_tweaks',
]


JQUERY_URL = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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
                'pages.context_processor.slider',
                'quizes.context_processor.total_correct_answer'
            ],
        },
    },
]


WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

FORCE_STATIC_FILE_SERVING = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myproject/static')
]


# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

ANSWER_SESSION_ID = 'answer'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'musficamurshidopshori@gmail.com'
EMAIL_HOST_PASSWORD = 'wgkjabbgcqluhuws'
EMAIL_PORT = 587


BATON = {
    'SITE_HEADER': 'StudentEvaluation Admin',
    'SITE_TITLE': 'StudentEvaluation Admin Portal',
    'INDEX_TITLE': 'Welcome to StudentEvaluation Researcher Portal',
    'SUPPORT_HREF': 'https://www.indstate.edu/',
    'COPYRIGHT': 'copyright © 2019 <a href="https://www.indstate.edu/">Indiana State University</a>',  # noqa
    'POWERED_BY': '<a href="https://www.indstate.edu"> Indiana State University</a>',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'MENU': (
        {'type': 'title', 'label': 'main', 'apps': ('auth', )},
        {
            'type': 'app',
            'name': 'auth',
            'label': 'Authentication',
            'icon': 'fa fa-lock',
            'models': (
                {
                    'name': 'user',
                    'label': 'Users'
                },
                {
                    'name': 'group',
                    'label': 'Groups'
                },
            )
        },
        {
            'type': 'app',
            'name': 'accounts',
            'label': 'Accounts',
            'icon': 'fa fa-user',
            'models': (
                {
                    'name': 'profile',
                    'label': 'Profiles'
                },
                {
                    'name': 'teacher',
                    'label': 'Teachers'
                },
                {
                    'name': 'student',
                    'label': 'Students'
                },
            )
        },
        {
            'type': 'app',
            'name': 'course',
            'label': 'Course',
            'icon': 'fa fa-university',
            'models': (
                {
                    'name': 'assignteacher',
                    'label': 'Assign Teachers'
                },
                {
                    'name': 'course',
                    'label': 'courses'
                },
                {
                    'name': 'evaluatestudent',
                    'label': 'Evaluate Students'
                },
                {
                    'name': 'studentcourse',
                    'label': 'Student Courses'
                },
            )
        },
        {
            'type': 'app',
            'name': 'programs',
            'label': 'Programs',
            'icon': 'fa fa-list',
            'models': (
                {
                    'name': 'department',
                    'label': 'Program'
                },
                {
                    'name': 'faculty',
                    'label': 'Department'
                },

            )
        },
        {
            'type': 'app',
            'name': 'session',
            'label': 'Session',
            'icon': 'fa fa-calendar-alt',
            'models': (
                {
                    'name': 'semester',
                    'label': 'Semester'
                },


            )
        },
        {
            'type': 'app',
            'name': 'pages',
            'label': 'Settings',
            'icon': 'fa fa-image',
            'models': (
                {
                    'name': 'sliderimage',
                    'label': 'Slider Image'
                },


            )
        },
        {
            'type': 'app',
            'name': 'quizes',
            'label': 'Quizes',
            'icon': 'fa fa-question-circle',
            'models': (
                {
                    'name': 'topic',
                    'label': 'Topic'
                },
                {
                    'name': 'question',
                    'label': 'Question'
                },
                {
                    'name': 'option',
                    'label': 'Option'
                },
            )
        },
        {
            'type': 'app',
            'name': 'boards',
            'label': 'Forum',
            'icon': 'fa fa-keyboard',
            'models': (
                {
                    'name': 'board',
                    'label': 'Channel'
                },
                {
                    'name': 'topic',
                    'label': 'Topic'
                },
                {
                    'name': 'post',
                    'label': 'Post'
                },


            )
        },


    ),
}
