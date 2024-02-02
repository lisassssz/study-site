from django import forms
from .models import Test, Question, Answer,Section
from .models import ExtraQuestion, ExtraAnswer

# class ExtraQuestionForm(forms.ModelForm):
#     class Meta:
#         model = ExtraQuestion
#         fields = ['question_text']

# class ExtraAnswerForm(forms.ModelForm):
#     class Meta:
#         model = ExtraAnswer
#         fields = ['answer_text', 'is_correct']

# class TestForm(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ['title', 'section']
    
#     def __init__(self, *args, **kwargs):
#         subject = kwargs.pop('subject', None)
#         super(TestForm, self).__init__(*args, **kwargs)
#         if subject:
#             self.fields['section'].queryset = Section.objects.filter(subject=subject)

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text']

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['answer_text', 'is_correct']
class QuestionForm(forms.Form):
    questions = forms.CharField(label='Вопрос', max_length=500, widget=forms.TextInput(attrs={'class': 'question-field'}))
    answers = forms.CharField(label='Ответ', max_length=500, widget=forms.TextInput(attrs={'class': 'answer-field'}))

class CreateTestForm(forms.Form):
    title = forms.CharField(label='Название теста', max_length=200)
    section = forms.ModelChoiceField(label='Раздел',queryset=Section.objects.all())  # Поле выбора раздела
    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super(CreateTestForm, self).__init__(*args, **kwargs)
        if subject:
            self.fields['section'].queryset = Section.objects.filter(subject=subject)

class EditTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'section']
        labels = {
            "title": "Название",
            "section": "Раздел",
        }
    