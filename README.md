<h1 align='center'>AlphaTrion</h1>

The Senate Website - AlphaTrion - is meant to be a tool for the Discovery High School student senate to preform data analytics on a school-wide scale. The website is to serve more than a single senate with an end goal of iteratively improving senate functions as time passes. The website is built to be modular without programming experience; senate members should be able to collect new data without having previous programming knowledge. With that in mind, the website is also to serve the purpose of data analytics, seamlessly visualizing data through the use of external libraries.

<h1 align='center'>Installation</h1>

##### Prerequisites
```
Python - 3.5.x (or newer)
Git - 2.13 (or newer)
```

##### Clone Repository

Open a command window in the location you would like to store the files and type in the following command:

```bash
git clone https://www.github.com/byrdofafeather/alphatrion
```

##### Installing Requirements

From the same directory type in: 

```bash
cd alphatrion
```

Then type the following commands to install the requirements: 

```bash
pip install -r requirements.txt
```

if on linux, type:

```bash
sudo pip install -r requirements.txt 
```

##### Setting up a Local Database
In the same directory (/alphatrion/) run the following command to setup a local database:

```py

python manage.py migrate

```

##### Fix Secret Key


```
Generate a secret key from https://www.miniwebtool.com/django-secret-key-generator/

```

Replace

```py
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '') 
```

With

```py
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'Insert Generated secret key here')
```

##### Fix Settings

Change:

```py

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
LOGIN_REDIRECT_URL = '/'

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# https://chrxr.com/django-error-logging-configuration-heroku/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}
```
To: 

```py

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# LOGIN_REDIRECT_URL = '/'

# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# # https://chrxr.com/django-error-logging-configuration-heroku/
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
#         },
#     },
# }
```

```
In models that require photos, S3DirectField must be changed to a file field as it requires https to work. 
```

##### Create SuperUser
In the /alphatrion/ directory, open a command window and type the following command:

```bash
python manage.py createsuperuser 
```

You will be prompted for user information, fill this out. This is the login for the /admin page

##### Verify Launch 
Finally, run 

```bash
python manage.py runserver
```

It will start the server and give you a link with a few numbers. Copy this into your browser and verify everything is working properly. 

<h1 align='center'>Built With</h1>


* [Django](https://www.djangoproject.com)
* [Bokeh](https://bokeh.pydata.org/en/latest/)
* [Vis.js](http://visjs.org)
* [Django-S3Direct](https://github.com/bradleyg/django-s3direct)
* [Nodejs](https://nodejs.org/en/)
* [Whitenoise](https://pypi.python.org/pypi/whitenoise)


<h1 align='center'>Authors</h1>

 * 2017-2018 School Year: 
 	* **Matthew Byrd** - *Initial Work* - [ByrdOfAFeather](https://www.github.com/byrdofafeather)

<h1 align='center'>License</h1>

MIT License - See [LICENSE.md](LICENSE.md) for details. 
