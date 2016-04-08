# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = "django_survey"

urlpatterns = [
    url(r"^(?P<token>[0-9a-zA-Z]{50})/answer/$", views.answer, name="answer"),
    url(r"^(?P<token>[0-9a-zA-Z]{50})/process_answer/$",
        views.process_answer, name="process_answer"),
    url(r"^(?P<token>[0-9a-zA-Z]{50})/finish/$",
        views.close_survey, name="close_survey"),
    ]
