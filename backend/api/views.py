from django.shortcuts import render

# This will handle our sentiment analysis endpoint 

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


from .utils.gpt2 import generate_text
from .utils.twitter import get_tweets
from .utils.google_nlp import analyze_text_sentiment
from .utils.sentiment_analysis_bert import SentimentAnalysisBERT
from .utils.dataset import GoEmotionDataset

from .models import Tweet
from .models import SentimentFeedback

def home(request):
    return render(request, 'index.html')


# This views,py autocomplete API Endpoint for Usernames
def search_usernames(request):
    if 'term' in request.GET:
        # First, get distinct users matching the search term
        qs = Tweet.objects.filter(user__icontains=request.GET.get('term')).values_list('user', flat=True).distinct()
        # Then, slice the queryset to limit the results
        usernames = list(qs[:10])
        return JsonResponse(usernames, safe=False)
    return JsonResponse([])


@api_view(['POST'])
def analyze_user_sentiment(request):
    
    # Get the username from the POST data
    username = request.data.get('username')
    if not username:
        return JsonResponse({'error': 'Username is required.'}, status=400)
    
    tweets = Tweet.objects.filter(user=username)

    #initializ einstances of the pytorch bert model and load the pretrained model from fine_tune_bert.py
    bert_model = SentimentAnalysisBERT(load_fine_tuned=True)

    # Analyze sentiment for each tweet
    tweet_sentiments = []
    for tweet in tweets:
        sentiment_result = analyze_text_sentiment(tweet.text)
        # Check if sentiment score is not None before processing
        if sentiment_result:
            if sentiment_result['score'] is not None:
                sentiment_score = sentiment_result['score']
                sentiment_label = determineSentimentLabel(sentiment_score)

                # usig this method of the bert model to predict the sentiment category of each tweet
                predicted_subcategory = bert_model.predict_sentiment_subcategory(tweet.text)
                tweet_sentiments.append({
                    'text': tweet.text,
                    'sentiment': {
                        'score': sentiment_score,
                        'label': sentiment_label,
                        'subcategory': predicted_subcategory
                    },
                    'created_at': tweet.date
                })

    # Calculate average sentiment score
    scores = []
    for s in tweet_sentiments:
        if s['sentiment']['score'] is not None:
            scores.append(s['sentiment']['score'])

    if scores:
        average_score = sum(scores) / len(scores)
        average_label = determineSentimentLabel(average_score)
    else:
        average_score = None
        average_label = 'Neutral'
    
    results = {
        'tweets': tweet_sentiments,
        'average_score': average_score,
        'average_label': average_label,
    }
    
    print(f"Predicted subcategory: {predicted_subcategory, tweet.text}")
    return JsonResponse(results)

def determineSentimentLabel(score):
    if score > 0.25:
        return 'positive'
    elif score < -0.25:
        return 'negative'
    else:
        return 'neutral'


@api_view(['POST'])
def submit_feedback(request):
    if request.method == 'POST':
        data = request.data

        tweet_id = data.get('tweet_id') 
        predicted_sentiment = data.get('predicted_sentiment')
        user_corrected_sentiment = data.get('user_corrected_sentiment')

        # Check if all required fields are present
        if tweet_id is None or predicted_sentiment is None or user_corrected_sentiment is None:
            return Response({'status': 'error', 'message': 'Missing required fields'}, status=400)


        # Create and save the feedback instance
        feedback = SentimentFeedback(
            tweet_id=tweet_id,
            predicted_sentiment=predicted_sentiment,
            user_corrected_sentiment=user_corrected_sentiment
        )
        feedback.save()

        return JsonResponse({'status': 'success', 'message': 'Feedback submitted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

'''

# MADE USE OF GPT 2.PY AND TWITTER.PY FILE TO BE MODIFIDIES LATER
@api_view(['GET', 'POST'])  # Allow both GET and POST requests
def analyze_user_sentiment(request):
    # For GET requests, use a default username or extract from query parameters
    if request.method == 'GET':
        username = request.query_params.get('username', 'default_username')
    else:  # POST request
        username = request.data.get('username', 'default_username')

    tweets = get_tweets(username)
    analyzed_tweets = [generate_text(tweet) for tweet in tweets]

    return JsonResponse({'tweets': analyzed_tweets})
'''