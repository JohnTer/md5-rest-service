EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

if MAIL_USE_TLS and MAIL_USE_SSL:
    raise Exception("Do not use both TLS and SSL")