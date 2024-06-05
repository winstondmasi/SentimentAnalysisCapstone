# Sentiment Analysis Capstone

Sentiment Analysis Capstone is a web application that analyzes and visualizes the sentiment of tweets over time. It leverages advanced sentiment analysis techniques and data visualization to provide users with valuable insights into the emotional landscape of Twitter.

## Features

- Sentiment analysis of tweets using a fine-tuned BERT model
- Visualization of sentiment trends over time
- Sentiment distribution pie chart
- Word cloud displaying most frequent words associated with sentiments
- Contribution graph heatmap showing sentiment patterns across months
- User feedback mechanism for sentiment analysis validation

## Dataset

The project utilizes two datasets for sentiment analysis:

1. **Sentiment140 Dataset**: This dataset, sourced from Kaggle, consists of 1.6 million tweets labeled as positive or negative. It serves as the foundation for training the sentiment analysis model.

2. **GoEmotions Dataset**: Developed by Google Research, the GoEmotions dataset provides a more fine-grained approach to sentiment analysis, categorizing text into 28 emotional categories. It is used to train the sentiment analysis model for more nuanced emotion detection.

## Prerequisites

Before running the application, ensure that you have the following dependencies installed:

- Python 3.x
- Django web framework
- Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository
2. Navigate to the project directory: 
    ```
    cd backend
    ```
3. Activate the virtual environment:
- For Windows:
  ```
  venv\Scripts\activate
  ```
- For macOS/Linux:
  ```
  source venv/bin/activate
  ```
4. Install the required dependencies: 
    ```
    pip install -r requirements.txt
    ```
5. Apply database migrations: 
    ```
    python manage.py migrate
    ```
6. Start the development server: 
    ```
    python manage.py runserver
    ```
7. Click "Kaggle Version" Button (current usable version)

## Usage

1. Enter a Twitter username in the search bar to analyze the sentiment of their tweets.
2. Explore the visualizations and gain insights into the emotional trends and patterns.
3. Provide feedback on the sentiment analysis results to help improve the model's accuracy.

## Future Enhancements

- Integration with Twitter API for real-time sentiment analysis
- User account management for personalized experiences
- Enhanced data visualization techniques
- Improved model performance and accuracy