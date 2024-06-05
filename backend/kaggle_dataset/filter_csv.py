import csv
from collections import Counter

# Path to the original CSV file
original_csv_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/training.1600000.processed.noemoticon.csv'

# Path to the new CSV file
filtered_csv_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/fitered.training.1194723.csv'

# Count the occurrences of each user
user_counts = Counter()
seen_ids = set()  # Set to keep track of seen ids

with open(original_csv_path, 'r', encoding='ISO-8859-1') as csvfile:
    columns = ['target', 'ids', 'date', 'flag', 'user', 'text']
    csv_reader = csv.DictReader(csvfile, fieldnames=columns)
    for row in csv_reader:
        user_counts[row['user']] += 1

# Write rows to new CSV, filtering both by user count and unique ids
with open(original_csv_path, 'r', encoding='ISO-8859-1') as csvfile, \
     open(filtered_csv_path, 'w', newline='', encoding='ISO-8859-1') as newfile:

    csv_reader = csv.DictReader(csvfile, fieldnames=columns)
    selected_columns = ['ids', 'date', 'user', 'text']
    csv_writer = csv.DictWriter(newfile, fieldnames=selected_columns, quoting=csv.QUOTE_ALL)

    csv_writer.writeheader()
    for row in csv_reader:
        if user_counts[row['user']] > 1 and row['ids'] not in seen_ids:
            filtered_row = {key: row[key] for key in selected_columns}
            csv_writer.writerow(filtered_row)
            seen_ids.add(row['ids'])  # Mark this ids as seen after writing the row

print("Filtered CSV created with users having multiple tweets.")


