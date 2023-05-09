# quiz_app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages

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

def quiz_creation(request):
    return render(request, 'quiz_app/quiz_creation.html')

def candidate_auth(request):
    return render(request, 'quiz_app/auth.html')

def quiz_results(request):
    return render(request, 'quiz_app/quiz_results.html')

def cand_results(request):
    return render(request, 'quiz_app/cand_results.html')

# Add more views for your other pages
