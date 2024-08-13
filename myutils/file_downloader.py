import os
import requests

def data_download(folder_path, file_name, url):
    file_path = os.path.join(folder_path, file_name)

    # Verificar se o arquivo já foi baixado
    if not os.path.exists(file_path):
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(folder_path, exist_ok=True)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path, True
        else:
            raise Exception(f"Erro ao baixar o arquivo. Status code: {response.status_code}")
    else:
        return file_path, False
