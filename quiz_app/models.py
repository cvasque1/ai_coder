from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, company_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, company_name=company_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, company_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, company_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    quizzes = models.ManyToManyField('Quiz', blank=True, related_name='quiz_creators')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name']

    def __str__(self):
        return self.email
    
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.PositiveIntegerField()
    questions = models.ManyToManyField('Question')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_quizzes')

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('TF', 'True/False'),
        ('MC', 'Multiple Choice'),
        ('CA', 'Check All That Apply'),
        ('FF', 'Free-form Answers'),
    )

    question_text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)

    def __str__(self):
        return self.question_text
    
class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
 