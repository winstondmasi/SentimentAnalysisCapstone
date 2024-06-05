# This will handle URL routing specific to our API

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'index'),
    path('sentiment/', views.analyze_user_sentiment, name='analyze_user_sentiment'), # GPT 2.PY FILE TO BE DELETED LATER
    path('search_usernames/', views.search_usernames, name='search_usernames'),
    path('analyze_sentiment/', views.analyze_user_sentiment, name='analyze_user_sentiment'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
]