import csv
from api.models import Tweet
from datetime import datetime
import pytz

# Function to parse tweet date string and convert it to a timezone-aware datetime object

def parse_tweet_date(date_str):
    # Split the date string by spaces
    parts = date_str.split()

    # Reconstruct the date string without the timezone abbreviation (PDT)
    # The format is: [Day of Week] [Month] [Day] [HH:MM:SS] [Year]
    date_str_no_tz = ' '.join([parts[0], parts[1], parts[2], parts[3], parts[5]])

    # Parse the date string into a naive datetime object (without timezone)
    date_without_tz = datetime.strptime(date_str_no_tz, '%a %b %d %H:%M:%S %Y')

    # Attach the 'America/Los_Angeles' timezone to the datetime object
    timezone = pytz.timezone('America/Los_Angeles')
    date_with_tz = timezone.localize(date_without_tz)

    return date_with_tz



csv_file_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/modified_dates_file.csv'

# Set the batch size and List to store tweetsfor bulk creation
batch_size = 1000  
tweets_to_create = []

with open(csv_file_path, 'r', encoding='ISO-8859-1') as csvfile:
    # Define the column names manually
    columns = ['ids','date', 'user', 'text']
    csv_reader = csv.DictReader(csvfile, fieldnames=columns)

    for row in csv_reader:
        try:
            # Parse the tweet date
            tweet_date = parse_tweet_date(row['date'])

            # Create a Tweet instance for each row in the CSV
            tweet = Tweet(
                ids=int(row['ids']),
                date=tweet_date,
                user=row['user'],
                text=row['text']
            )

            # Append the tweet instance to the list
            tweets_to_create.append(tweet)
            
            # Bulk create when the list size reaches the batch size
            if len(tweets_to_create) >= batch_size:
                Tweet.objects.bulk_create(tweets_to_create)
                tweets_to_create = []  # Reset the list after a batch save
        except Exception as e:
            print(f"Failed to import tweet at row {csv_reader.line_num}: {e}")
            print(f"Row data: {row}")


# Bulk create any remaining tweets after the loop
if tweets_to_create:
    Tweet.objects.bulk_create(tweets_to_create)
