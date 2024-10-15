import requests
import json

# Путь к JSON-файлу с моковыми данными
json_file_path = 'D:/pet/ranoberead/server/output.json'

# URL-адрес эндпоинта для глав
chapter_url = 'http://localhost:8080/api/chapters'


ranobe_id = "670921dbdad01c7a159da9d6"
# Загрузка данных из файла
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Загрузка Chapters данных
for chapter in data['chapter']:
    response = requests.post(chapter_url, json={
        "ranobe_id": ranobe_id,
        "chapter_id": chapter['chapter_id'],
        "chapter_number_origin": chapter['chapter_number_origin'],
        "title_ru": chapter['title_ru'],
        "title_en": chapter['title_en'],
        "content_ru": chapter['content_ru'],
        "content_en": chapter['content_en']
    })
    print(f"Chapter: {chapter['title_en']} -> {response.status_code}, Response: {response.text}")
