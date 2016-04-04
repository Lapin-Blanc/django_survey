import random
import string
from datetime import datetime

from django.db import models
from django.template.defaultfilters import date as _date
from django.core.urlresolvers import reverse

from .google_mail import send_email


class MailConfig(models.Model):

    name = models.CharField("Nom", max_length=50)
    domain = models.CharField("Domaine", max_length=50)
    sender = models.EmailField("Expéditeur")
    password = models.CharField("Mot de passe", max_length=20)
    subject = models.CharField("Objet", max_length=100)
    message = models.TextField(
        "Message",
        blank=True,
        default="Corps du message")

    class Meta:
        verbose_name = "Configuration de messagerie"
        verbose_name_plural = "Configurations de messagerie"

    def __str__(self):
        return self.name


class Questionnaire(models.Model):

    title = models.CharField("Titre", max_length=200)
    mail_config = models.ForeignKey(
        MailConfig,
        verbose_name="Configuration de la messagerie"
        )

    class Meta:
        verbose_name = "questionnaire"
        verbose_name_plural = "questionnaires"

    def __str__(self):
        return self.title


class Question(models.Model):

    question_text = models.CharField("Question", max_length=200)
    record = models.BooleanField("Question récapitulative ?", default=False)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return self.question_text


class Survey(models.Model):

    token = models.SlugField(max_length=50, blank=True)
    subject = models.CharField("Objet de l'enquête", max_length=100)
    firstname = models.CharField(
        "Prénom", max_length=50, blank=True)
    lastname = models.CharField("nom", max_length=50, blank=True)
    email = models.EmailField("Adresse mail")
    event_date = models.DateField("Date évènement", null=True, blank=True)
    date_sent = models.DateField("Date d'envoi", null=True, blank=True)
    date_received = models.DateField(
        "Date de réception", null=True, blank=True)
    sent = models.BooleanField("Envoyé", default=False)
    questionnaire = models.ForeignKey(Questionnaire)
    current_questionnaire = models.IntegerField(null=True, blank=True)
    remarks = models.TextField("Remarques", blank=True)
    suggestions = models.TextField("Suggestions", blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = ''.join(
                random.sample(string.ascii_letters + string.digits, 50))
        if not self.sent:
            html_subject = self.prepare_message(
                self.questionnaire.mail_config.subject)
            html_message = self.prepare_message(
                self.questionnaire.mail_config.message)
            send_email(
                self.questionnaire.mail_config.sender,
                self.questionnaire.mail_config.password,
                self.email,
                html_subject,
                html_message)
            self.date_sent = datetime.today()
            self.sent = True
        super().save(*args, **kwargs)

        if (self.current_questionnaire and
                (self.questionnaire.id != self.current_questionnaire)):
            self.surveyquestion_set.all().delete()
        self.current_questionnaire = self.questionnaire.id
        super().save(*args, **kwargs)
        if not self.surveyquestion_set.all().count():
            for question in self.questionnaire.question_set.all():
                self.surveyquestion_set.create(
                    question_text=question.question_text,
                    record=question.record)

    def completed(self):
        return len(self.surveyquestion_set.filter(score__isnull=True)) == 0
    completed.boolean = True
    completed.short_description = 'Complétée'

    class Meta:
        verbose_name = "Enquête"
        verbose_name_plural = "Enquêtes"

    def __str__(self):
        return ", ".join([self.subject, self.email])

    def prepare_message(self, message):
        html_message = message.replace("\r\n", "<br />")
        survey_link = "".join(
                [
                    self.questionnaire.mail_config.domain,
                    reverse("django_survey:answer", args=(self.token,))
                ]
            )
        html_message = html_message.replace(
            "#LINK#",
            '<a href="%s">lien vers l\'enquête</a>' % survey_link)
        html_message = html_message.replace(
            "#SUBJECT#",
            self.subject)
        html_message = html_message.replace(
            "#EVENT_DATE#",
            _date(self.event_date, "d F Y"))
        html_message = html_message.replace(
            "#FIRSTNAME#",
            self.firstname)
        html_message = html_message.replace(
            "#LASTNAME#",
            self.lastname)
        return html_message


class SurveyQuestion(models.Model):

    question_text = models.CharField("Question", max_length=200)
    record = models.BooleanField("Question récapitulative ?", default=False)
    score = models.IntegerField(null=True, blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return ""
