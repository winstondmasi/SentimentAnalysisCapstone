import torch
from transformers import BertTokenizer, BertForSequenceClassification
from tqdm import tqdm

class SentimentAnalysisBERT:
    def __init__(self, load_fine_tuned=True):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        
        if load_fine_tuned:
            self.model = BertForSequenceClassification.from_pretrained('/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/api/utils/saved-model')
        else:
            self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=28)
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        self.label_map = {
            'admiration': 0, 'amusement': 1, 'anger': 2, 'annoyance': 3, 'approval': 4, 'caring': 5,
            'confusion': 6, 'curiosity': 7, 'desire': 8, 'disappointment': 9, 'disapproval': 10,
            'disgust': 11, 'embarrassment': 12, 'excitement': 13, 'fear': 14, 'gratitude': 15,
            'grief': 16, 'joy': 17, 'love': 18, 'nervousness': 19, 'optimism': 20, 'pride': 21,
            'realization': 22, 'relief': 23, 'remorse': 24, 'sadness': 25, 'surprise': 26, 'neutral': 27
        }
        
        self.id_to_label = {v: k for k, v in self.label_map.items()}
    
    def predict_sentiment_subcategory(self, text):
        """
        Predict the specific sentiment subcategory for the given text and sentiment label.
        """
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_subcategory_id = torch.argmax(logits, dim=1).item()
        predicted_subcategory = self.id_to_label[predicted_subcategory_id]
        return predicted_subcategory
    
    def fine_tune(self, train_dataset, epochs=3, batch_size=16, learning_rate=2e-5):
        """
        Fine-tune the BERT model on the provided training dataset.
        """
        train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=self.collate_fn)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=learning_rate)
        self.model.train()

        for epoch in range(epochs):
            progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}", unit="batch")
            for batch in progress_bar:
                inputs = {k: v.to(self.device) for k, v in batch.items() if k != 'label'}
                labels = batch['label'].to(self.device)
                optimizer.zero_grad()
                outputs = self.model(**inputs, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                progress_bar.set_postfix({"Loss": loss.item()})

            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")
    
    def collate_fn(self, batch):
        """
        Collate function to process the data batch and return a dictionary of tensors.
        """
        texts = [item['text'] for item in batch]
        labels = [self.label_map[item['label']] for item in batch]

        inputs = self.tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
        labels = torch.tensor(labels)

        return {'input_ids': inputs['input_ids'], 'attention_mask': inputs['attention_mask'], 'label': labels}