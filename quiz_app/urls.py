# quiz_app/urls.py

from django.urls import path
from . import views
from .views import CreateQuizView

app_name = 'quiz_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth_page, name='auth_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quizzespage/', views.quizzes_page, name='quizzespage'),
    path('editquizpage/<int:quiz_id>', views.edit_quiz_page, name='editquizpage'),
    path('create_quiz/', CreateQuizView.as_view(), name='create_quiz'),
    path('available_questions/', views.available_questions, name='available_questions'),
    # path('create/', views.quiz_creation, name='quiz_creation'),
    path('candidate_auth/', views.candidate_auth, name='candidate_auth'),
    path('candidatespage', views.candidates_page, name='candidatespage'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('cand_results/', views.cand_results, name='cand_results'),
    path('resultspage', views.results_page, name='resultspage'),

    # Add more paths for your other pages
]
 