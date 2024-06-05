from django.db import models

# Create your models here.
class Tweet(models.Model):
    
    ids = models.BigIntegerField(primary_key=True)
    date = models.DateTimeField()
    user = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.text
    
class GoEmotion(models.Model):
    text = models.TextField()
    data_id = models.CharField(max_length=255, unique=True, primary_key=True)
    author = models.CharField(max_length=255)
    subreddit = models.CharField(max_length=255)
    link_id = models.CharField(max_length=255)
    parent_id = models.CharField(max_length=255)
    created_utc = models.CharField(max_length=255)  
    rater_id = models.CharField(max_length=255)
    example_very_unclear = models.BooleanField(default=False)

    # Emotional categories
    admiration = models.BooleanField(default=False)
    amusement = models.BooleanField(default=False)
    anger = models.BooleanField(default=False)
    annoyance = models.BooleanField(default=False)
    approval = models.BooleanField(default=False)
    caring = models.BooleanField(default=False)
    confusion = models.BooleanField(default=False)
    curiosity = models.BooleanField(default=False)
    desire = models.BooleanField(default=False)
    disappointment = models.BooleanField(default=False)
    disapproval = models.BooleanField(default=False)
    disgust = models.BooleanField(default=False)
    embarrassment = models.BooleanField(default=False)
    excitement = models.BooleanField(default=False)
    fear = models.BooleanField(default=False)
    gratitude = models.BooleanField(default=False)
    grief = models.BooleanField(default=False)
    joy = models.BooleanField(default=False)
    love = models.BooleanField(default=False)
    nervousness = models.BooleanField(default=False)
    optimism = models.BooleanField(default=False)
    pride = models.BooleanField(default=False)
    realization = models.BooleanField(default=False)
    relief = models.BooleanField(default=False)
    remorse = models.BooleanField(default=False)
    sadness = models.BooleanField(default=False)
    surprise = models.BooleanField(default=False)
    neutral = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class SentimentFeedback(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True, blank=True)
    predicted_sentiment = models.CharField(max_length=50)
    user_corrected_sentiment = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tweet} - {self.user_corrected_sentiment}"
