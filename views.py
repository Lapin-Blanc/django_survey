# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Survey


def answer(request, token, error=False):
    survey = get_object_or_404(Survey, token=token)
    if survey.completed():
        return HttpResponseRedirect(
            reverse("django_survey:close_survey", args=(token,)))
    else:
        if error:
            error_message = "Veuillez répondre aux questions "
            "suivantes pour compléter l'enquête"
        else:
            error_message = None
        return render(
            request, "django_survey/answer.html",
            context={"survey": survey, "error_message": error_message})


def process_answer(request, token):
    survey = get_object_or_404(Survey, token=token)
    if survey.completed():
        return HttpResponseRedirect(
            reverse("django_survey:close_survey", args=(token,)))

    for q in survey.surveyquestion_set.filter(score__isnull=True):
        try:
            score = request.POST[str(q.id)]
            q.score = score
            q.save()
        except KeyError:
            pass
    survey.remarks = request.POST["remarks"]
    survey.suggestions = request.POST["suggestions"]
    survey.save()

    not_answered_questions = survey.surveyquestion_set.filter(
        score__isnull=True).count()
    if not_answered_questions > 0:
        return answer(request, token, error=True)
    survey.date_received = datetime.today()
    survey.save()
    return HttpResponseRedirect(
        reverse("django_survey:close_survey", args=(token,)))


def close_survey(request, token):
    survey = get_object_or_404(Survey, token=token)
    return render(
        request, "django_survey/finish.html",
        context={"survey": survey}
        )
