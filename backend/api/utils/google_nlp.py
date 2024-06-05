import os
from google.cloud import language_v1
from google.oauth2 import service_account

def analyze_text_sentiment(text):
    # Retrieve the path to the credentials from the environment variable
    path_to_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if not path_to_credentials:
        raise ValueError("No credentials file found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    
    # Authenticate and create a client for the Google Natural Language API
    # Prepare the document with the text to analyze
    credentials = service_account.Credentials.from_service_account_file(path_to_credentials)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    # analyze the sentiment of the text by making API request
    try:
        
        response = client.analyze_sentiment(request={'document': document})
        
        # Extract the overall sentiment score and magnitude from the response
        sentiment = response.document_sentiment
        return {
            'score': sentiment.score,  # Sentiment score ranges between -1.0 (negative) and 1.0 (positive)
            'magnitude': sentiment.magnitude  # Magnitude indicates the overall strength of emotion in the text
        }
    except Exception as e:
        # If an error occurs return None values
        print(f"Failed to analyze text sentiment: {e}")
        return {'score': None, 'magnitude': None}
