from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Quiz, Question

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['company_name', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'time_limit', 'questions')
        widgets = {
            'questions': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questions'].queryset = Question.objects.all()


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'time_limit', 'questions')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']
