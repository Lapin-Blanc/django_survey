from django.contrib import admin
from django import forms
from .models import Questionnaire, Question, MailConfig, Survey, SurveyQuestion


class MailConfigForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = MailConfig
        fields = ('name', 'domain', 'sender', 'password', 'subject', 'message')


class MailConfigAdmin(admin.ModelAdmin):
    model = MailConfig
    form = MailConfigForm

admin.site.register(MailConfig, MailConfigAdmin)


class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=forms.TextInput(attrs={'size': '120'}))

    class Meta:
        model = Question
        fields = ('question_text', 'record')


class QuestionsInline(admin.TabularInline):
    model = Question
    form = QuestionForm
    fields = ['question_text', 'record']
    extra = 0


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline]

admin.site.register(Questionnaire, QuestionnaireAdmin)


class SurveyQuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=forms.TextInput(attrs={'size': '120'}))

    class Meta:
        model = SurveyQuestion
        fields = ('question_text', 'record', 'score')


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    form = SurveyQuestionForm
    fields = ['question_text', 'record', 'score']
    readonly_fields = ['question_text', 'record']
    can_delete = False
    extra = 0

    def has_add_permission(self, request):
        return False


class SurveyAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject', 'sent', 'completed']
    readonly_fields = ['token']
    inlines = [SurveyQuestionInline]

admin.site.register(Survey, SurveyAdmin)
