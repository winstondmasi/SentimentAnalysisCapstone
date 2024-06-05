import pandas as pd

file_paths = ['/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/full_dataset_copy/goemotions_1.csv',
              '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/full_dataset_copy/goemotions_2.csv',
              '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/full_dataset_copy/goemotions_3.csv']
output_path = '/Users/winstondennis-masi/repo/23-24_CE301_dennis-masi_winston_c-2/backend/full_dataset_copy/goemotions_final.csv'

df = pd.read_csv(file_paths[0])
for file_path in file_paths[1:]:
    df_temp = pd.read_csv(file_path, header=None, skiprows=1)
    df_temp.columns = df.columns
    df = pd.concat([df, df_temp])

df.to_csv(output_path, index=False)

print("Combined CSV saved as 'goemotions_final.csv'")
