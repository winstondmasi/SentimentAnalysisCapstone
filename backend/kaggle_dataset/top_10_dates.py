import csv
from collections import Counter

csv_file_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/fitered.training.1194723.csv'

username_counter = Counter()

with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        username = row[2]
        username_counter[username] += 1

usernames_in_range = [(username, count) for username, count in username_counter.items() if 30 <= count <= 50]

for username, count in usernames_in_range:
    print(f'Username: {username}, Count: {count}')

