# django_survey
Django app for surveys

## deployment
    mkdir SurveySite
    cd SurveySite/
    virtualenv -p /usr/bin/python3 .
    . bin/activate
    pip install django pytz
    django-admin startproject MySite
    mv MySite/ srcmv MySite/ src
    cd src
    git clone https://github.com/Lapin-Blanc/django_survey.git
    vim MySite/settings.py

add django_survey app, adjust localization

    vim MySite/urls.py

## on test server
    from django.conf.urls import url, include
    from django.contrib import admin
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^survey/', include('django_survey.urls')),
    ]

    urlpatterns += staticfiles_urlpatterns()

## configure and launch app
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver 0.0.0.0:8000
    
