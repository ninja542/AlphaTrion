from django import forms
from django.core.exceptions import ValidationError
from .models import Questions, CustomSurvey, SurveyQuestions, AnswerInt, AnswerText, SenateProjects


# https://github.com/jessykate/django-survey
class CustomSurveyForm(forms.ModelForm):
	class Meta:
		model = CustomSurvey
		exclude = ('title', 'date', 'author', 'questions')

	def __init__(self, *args, **kwargs):
		customsurvey = kwargs.pop('survey')
		self.user = kwargs.pop('user')
		self.customsurvey = customsurvey
		super(CustomSurveyForm, self).__init__(*args, **kwargs)

		data = kwargs.get('data')

		for questions in customsurvey.questions.all():
			if questions.question_type == Questions.TEXT:
				self.fields['question_{}'.format(questions.pk)] = forms.CharField(label=questions.question, widget=forms.Textarea)
			elif questions.question_type == Questions.INTEGER:
				self.fields['question_{}'.format(questions.pk)] = forms.IntegerField(label=questions.question)

			if questions.required:
				self.fields['question_{}'.format(questions.pk)].required = True
				self.fields['question_{}'.format(questions.pk)].widget.attrs['class'] = 'required'
			else:
				self.fields['question_{}'.format(questions.pk)].required = False

			if data:
				self.fields['question_{}'.format(questions.pk)].initial = data.get(questions.question)

	
	def save(self, commit=True):
		for questions, answer in self.cleaned_data.items():
			if questions.startswith('question_'):
				question = Questions.objects.get(pk=questions.split('_')[1])
				survey = CustomSurvey.objects.get(pk=self.customsurvey.pk)

				if question.question_type == Questions.TEXT:
					a = AnswerText(question=question, user=self.user, survey=survey, answer=answer)

				elif question.question_type == Questions.INTEGER:
					a = AnswerInt(question=question, user=self.user, survey=survey, answer=answer)
					
				a.save()