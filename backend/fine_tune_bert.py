import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.utils.sentiment_analysis_bert import SentimentAnalysisBERT
from api.utils.dataset import GoEmotionDataset

def fine_tune_bert():
    bert_model = SentimentAnalysisBERT()
    train_dataset = GoEmotionDataset()
    bert_model.fine_tune(train_dataset, epochs=3, batch_size=16, learning_rate=2e-5)
    bert_model.model.save_pretrained('/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/api/utils/saved-model')

if __name__ == '__main__':
    fine_tune_bert()