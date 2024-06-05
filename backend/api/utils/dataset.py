from api.models import GoEmotion
from torch.utils.data import Dataset

class GoEmotionDataset(Dataset):
    def __init__(self):
        self.data = []
        self.label_map = self._create_label_map()
        self._load_data()

    def _create_label_map(self):
        """
        Create a mapping between sentiment labels and their corresponding indices.
        """
        labels = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion',
            'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment',
            'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism',
            'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral'
        ]
        return {label: i for i, label in enumerate(labels)}

    def _load_data(self):
        """
        Load the sentiment data from the GoEmotion model and preprocess it.
        """
        emotions = GoEmotion.objects.all()
        print("Loaded emotions count:", len(emotions))
        for emotion in emotions:
            text = emotion.text
            label = self._get_label(emotion)
            if label is not None:
                self.data.append({'text': text, 'label': label})
        print("Total data loaded:", len(self.data))

    def _get_label(self, emotion):
        """
        Get the sentiment label index for a given emotion instance.
        """
        for label, index in self.label_map.items():
            if getattr(emotion, label): 
                return label
        return None


    def __len__(self):
        """
        Return the length of the dataset.
        """
        return len(self.data)

    def __getitem__(self, index):
        """
        Return a single data item at the given index.
        """
        return self.data[index]