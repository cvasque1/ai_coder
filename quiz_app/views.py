# quiz_app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from .forms import CustomUserCreationForm, CreateQuizForm, QuizForm, QuestionForm
from .models import Quiz, Question
import json

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            # login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('quiz_app:auth_page')
        else:
            messages.error(request, "Registration failed. Please try again.")
            print(form.errors)
            return redirect('quiz_app:auth_page')
    else:
        form = CustomUserCreationForm()
    return render(request, 'quiz_app/loginpage.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect the user to the dashboard after successful login
            return redirect('quiz_app:dashboard')
        else:
            # Redirect back to the auth_page with an error message if authentication fails
            messages.error(request, 'Invalid username or password')
            return redirect('quiz_app:auth_page')
    else:
        return redirect('quiz_app:auth_page')

 
def home(request):
    return render(request, 'quiz_app/homev2.html')

def auth_page(request):
    return render(request, 'quiz_app/loginpage.html')

def dashboard(request):
    return render(request, 'quiz_app/dashboard.html')

def quizzes_page(request):
    user = request.user
    user_quizzes = Quiz.objects.filter(owner=user)
    form = CreateQuizForm()
    return render(request, 'quiz_app/quizzespage.html', {'quizzes': user_quizzes, 'form': form})

def fetch_quizzes(request):
    user = request.user
    user_quizzes = Quiz.objects.filter(owner=user)
    html = render_to_string('quiz_app/quizzes_list.html', {'quizzes': user_quizzes})
    response_data = {'status': 'success', 'html': html}
    return JsonResponse(response_data)

class CreateQuizView(View):
    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = CreateQuizForm(request.POST)
            print(request.POST)
            if form.is_valid():
                quiz = form.save(commit=False)
                quiz.owner = request.user
                quiz.save()
                # Get the selected questions from the request
                selected_questions = request.POST.getlist('questions')
                # Add the selected questions to the quiz
                for question_id in selected_questions:
                    question = Question.objects.get(id=question_id)
                    quiz.questions.add(question)
                quiz.save()
                return JsonResponse({'status': 'success', 'message': 'Quiz created successfully.'})
            else:
                print(form.errors)
                messages.error(request, "Quiz creation failed. Please try again.")
                return JsonResponse({'status': 'error', 'message': 'Form is not valid.'})
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def edit_quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
    
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = CreateQuizForm(request.POST, instance=quiz)
            if form.is_valid():
                quiz = form.save(commit=False)
                quiz.save()
                question_ids = json.loads(request.POST.get('question_ids', '[]'))
                quiz.questions.set(Question.objects.filter(id__in=question_ids))
                return JsonResponse({'status': 'success', 'message': 'Quiz updated successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Form is not valid.'})
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    form = CreateQuizForm(instance=quiz)
    questions = quiz.questions.all()
    available_questions = Question.objects.all()
    questions_data = [model_to_dict(question) for question in questions]
    available_questions_data = [model_to_dict(question) for question in available_questions]
    
    context = {
        'form': form,
        'questions': json.dumps(questions_data),
        'available_questions': json.dumps(available_questions_data)
    }
    return render(request, 'quiz_app/editquizpage.html', context)

def available_questions(request):
    search_term = request.GET.get('search', '')
    question_type = request.GET.get('question_type', '')

    # Fetch questions that are not in the quiz
    available_questions = Question.objects.exclude(quiz__id=request.GET.get('quiz_id'))

    if search_term:
        available_questions = available_questions.filter(question_text__icontains=search_term)

    if question_type:
        available_questions = available_questions.filter(question_type=question_type)

    return render(request, 'quiz_app/available_questions.html', {'questions': available_questions})


def candidates_page(request):
    return render(request, 'quiz_app/candidatespage.html')

def results_page(request):
    return render(request, 'quiz_app/resultspage.html')

def quiz_creation(request):
    return render(request, 'quiz_app/quiz_creation.html')

def candidate_auth(request):
    return render(request, 'quiz_app/candidate_auth.html')

def quiz_results(request):
    return render(request, 'quiz_app/quiz_results.html')

def cand_results(request):
    return render(request, 'quiz_app/cand_results.html')

# Add more views for your other pages
