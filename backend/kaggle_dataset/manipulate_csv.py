import csv
from datetime import datetime, timedelta
import random


csv_file_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/fitered.training.1194723.csv'
output_file_path = 'modified_dates_file.csv'

# Function to generate a random date in 2009
def generate_random_date():
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month == 2:
        day = random.randint(1, 28)  # 2009 is not a leap year
    else:
        day = random.randint(1, 30)
    
    return datetime(year=2009, month=month, day=day)

with open(csv_file_path, 'r', encoding='utf-8') as csvfile, open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
    csv_reader = csv.reader(csvfile)
    csv_writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    
    for row in csv_reader:
        original_date_str = row[1]
        original_date = datetime.strptime(original_date_str, "%a %b %d %H:%M:%S PDT %Y")
        
        new_date = generate_random_date().replace(hour=original_date.hour, minute=original_date.minute, second=original_date.second)

        new_date_str = new_date.strftime("%a %b %d %H:%M:%S PDT %Y")
        
        row[1] = new_date_str

        csv_writer.writerow(row)
