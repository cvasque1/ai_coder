# quiz_app/urls.py

from django.urls import path
from . import views

app_name = 'quiz_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth_page, name='auth_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.quiz_creation, name='quiz_creation'),
    path('candidate_auth/', views.candidate_auth, name='candidate_auth'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('cand_results/', views.cand_results, name='cand_results'),
    # Add more paths for your other pages
]
 