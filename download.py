from myutils import data_download ## manter todos os dados no googledrive
import pandas as pd

def func(row):
    id = row['id']
    folder_path = row['folder_path']
    file_name = row['filename']
    url = 'https://drive.google.com/uc?export=download&id=' + id
    (path,_) = data_download(folder_path, file_name, url)
    print (path)
    
df = pd.read_csv('files_id.csv', sep=";")
df.head()

for index, row in df.iterrows():
    func(row)