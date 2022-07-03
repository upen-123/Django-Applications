DEBUG = True

ALLOWED_HOSTS = ['*']

# Database

# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.mysql",

        "NAME": "jcms_db",

        "USER": "root",

        "PASSWORD": "mynewpassword",

        "HOST": "localhost",

        "PORT": 3306

    }

}

# Basic Auth for Microservices

BASICAUTH_USERS = {

    'dashboard': 'dashboard@123!@'

}

CASSANDRA_DB = {

    "CASSANDRA_DB": {

        "HOSTNAME": "10.159.17.158,10.159.17.159,10.159.17.160",

        "USERNAME": "dev_jcms_devices_rw",

        "PASSWORD": "JcmsRw!@345",

        "NAME": "jcms_devices",

        "RW_KEYSPACE": "jcms_processed_data",

        "R_KEYSPACE": "jcms_devices"

    }

}

# jwt secret keys

JWT_PRIVATE_KEY = "/home/upendra/Desktop/jwtRS256.key"

JWT_PUBLIC_KEY = "/home/upendra/Desktop/jwtRS256.key.pub"

JWT_ALGORITHM = "RS256"

JWT_EXP_DELTA_SECONDS = 15000  # 5hours

app_log_path = "/home/upendra/Desktop/debug.log"

debug_log_path = "/home/upendra/Desktop/debug.log"

# email configurations

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "10.157.212.66"

EMAIL_PORT = 25

EMAIL_HOST_USER = "Noreply-jiophone@jio.com"

COMM_EMAIL_SENDER = "Noreply-jiophone@jio.com"

REDIS_SENTINEL_SERVER = {"HOSTNAME": ["localhost"], "PORT": 26379, "BROKER_DB": 0, "PASSWORD": "", "OTP_DB": 1,
                         "MASTER_NAME": "mymaster"}

# Twilio Server

TWILIO_ACCOUNT_SID = "ACe5027ca5fc592267693976cbeed6b011"

TWILIO_AUTH_TOKEN = "ee83480cdacbdbf38739240788da46ef"

TWILIO_FROM_NUMBER_SMS = "SMSsys"

# SMS Configurations

SMS_HOST = "10.55.79.162"

SMS_PORT = 9000

SMS_USERNAME = "ccarusrm"

SMS_PASSWORD = "jio12345"

SMS_SOURCE_ADDRESS = "0"

# celery backend and broker config

CELERY_REDIS_BROKER = "redis://:%s@%s:%s/%s" % (

    REDIS_SENTINEL_SERVER["PASSWORD"],

    REDIS_SENTINEL_SERVER["HOSTNAME"],

    REDIS_SENTINEL_SERVER["PORT"],

    REDIS_SENTINEL_SERVER["BROKER_DB"],

)

CELERY_RESULT_BACKEND = CELERY_REDIS_BROKER

# Logging configuration

# See https://docs.djangoproject.com/en/1.11/topics/logging/
HOSTNAME=""

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "filters": {

        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},

        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},

    },

    "formatters": {

        "main_formatter": {

            "format": "%(levelname)s:%(name)s: %(message)s " "(%(asctime)s; %(filename)s:%(lineno)d)",

            "datefmt": "%Y-%m-%d %H:%M:%S",

        }

    },

    "handlers": {

        "console": {

            "level": "INFO",

            "filters": ["require_debug_true"],

            "class": "logging.StreamHandler",

            "formatter": "main_formatter",

        },

        "django.server": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "main_formatter"},

        "file_log": {

            "level": "INFO",

            "class": "logging.handlers.RotatingFileHandler",

            "filename": app_log_path,

            "maxBytes": 1024 * 1024 * 5,  # 5 MB

            "backupCount": 50,

            "filters": ["require_debug_false"],

            "formatter": "main_formatter",

        },

        "debug_file": {

            "level": "DEBUG",

            "class": "logging.handlers.RotatingFileHandler",

            "filename": debug_log_path,

            "maxBytes": 1024 * 1024 * 5,  # 5 MB

            "backupCount": 0,

            "filters": ["require_debug_true"],

            "formatter": "main_formatter",

        },

    },

    "loggers": {

        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},

        "": {"handlers": ["console", "file_log", "debug_file"], "level": "INFO"},

        "django.server": {"handlers": ["django.server"], "level": "INFO", "propagate": False},

    },

}

SECRET_KEY = "c=*gswjgm&rup&9p%y2wd@4^!!s#^jyh2hasrlu-4%9wyn((^p"

REDIS_KEY_EXPIRY = 600  # in seconds
JWT_WEB_EXP_DELTA_HOURS = 543
OTP_LENGTH = 4
