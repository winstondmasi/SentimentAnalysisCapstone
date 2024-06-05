import csv
from api.models import GoEmotion
from django.db import transaction 
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

file_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/full_dataset_copy/goemotions_final.csv'

goemotions_instances = []
batch_size = 1000

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        instance = GoEmotion(
            text=row['text'],
            data_id=row['id'],
            author=row['author'],
            subreddit=row['subreddit'],
            link_id=row['link_id'],
            parent_id=row['parent_id'],
            created_utc=row['created_utc'],
            rater_id=row['rater_id'],
            example_very_unclear=row.get('example_very_unclear', 'False') == 'True',
            admiration=row.get('admiration', '0') == '1',
            amusement=row.get('amusement', '0') == '1',
            anger=row.get('anger', '0') == '1',
            annoyance=row.get('annoyance', '0') == '1',
            approval=row.get('approval', '0') == '1',
            caring=row.get('caring', '0') == '1',
            confusion=row.get('confusion', '0') == '1',
            curiosity=row.get('curiosity', '0') == '1',
            desire=row.get('desire', '0') == '1',
            disappointment=row.get('disappointment', '0') == '1',
            disapproval=row.get('disapproval', '0') == '1',
            disgust=row.get('disgust', '0') == '1',
            embarrassment=row.get('embarrassment', '0') == '1',
            excitement=row.get('excitement', '0') == '1',
            fear=row.get('fear', '0') == '1',
            gratitude=row.get('gratitude', '0') == '1',
            grief=row.get('grief', '0') == '1',
            joy=row.get('joy', '0') == '1',
            love=row.get('love', '0') == '1',
            nervousness=row.get('nervousness', '0') == '1',
            optimism=row.get('optimism', '0') == '1',
            pride=row.get('pride', '0') == '1',
            realization=row.get('realization', '0') == '1',
            relief=row.get('relief', '0') == '1',
            remorse=row.get('remorse', '0') == '1',
            sadness=row.get('sadness', '0') == '1',
            surprise=row.get('surprise', '0') == '1',
            neutral=row.get('neutral', '0') == '1',
        )
        goemotions_instances.append(instance)
        
        if len(goemotions_instances) >= batch_size:
            with transaction.atomic():
                GoEmotion.objects.bulk_create(goemotions_instances, ignore_conflicts=True)
                goemotions_instances = [] 

if goemotions_instances:
    with transaction.atomic():
        GoEmotion.objects.bulk_create(goemotions_instances, ignore_conflicts=True)

print("Data import completed.")
