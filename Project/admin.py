from django.contrib import admin
from .models import SurveyQuestions, AnswerText, AnswerInt, CustomSurvey, Questions, SenateProjects

@admin.register(SurveyQuestions)
class SurveyQuestionsAdmin(admin.ModelAdmin):
	model = SurveyQuestions

@admin.register(AnswerText)
class AnswerTextAdmin(admin.ModelAdmin):
	model = AnswerText

@admin.register(AnswerInt)
class AnswerIntAdmin(admin.ModelAdmin):
	model = AnswerInt

@admin.register(CustomSurvey)
class CustomSurveyAdmin(admin.ModelAdmin):
	model = CustomSurvey

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
	model = Questions

@admin.register(SenateProjects)
class SenateProjectsAdmin(admin.ModelAdmin):
	model = SenateProjects

