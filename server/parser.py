import requests
from bs4 import BeautifulSoup
import json

# Настройки парсера
BASE_URL = "https://wtr-lab.com/en/serie-619/losing-money-to-be-a-tycoon/chapter-{}"
START_CHAPTER = 337
NUM_CHAPTERS = 5
RANOBE_ID = 1  # ID существующего ранобэ в базе данных

# URL вашего API для создания новой главы
API_URL = "http://localhost:5000/chapters"  # Измените на актуальный URL вашего API

def fetch_chapter_content(chapter_number):
    url = BASE_URL.format(chapter_number)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch chapter {chapter_number}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем скрипт с данными JSON
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        print(f"Could not find JSON data for chapter {chapter_number}")
        return None
    
    # Извлекаем и парсим JSON
    json_data = json.loads(script_tag.string)
    
    # Пытаемся найти содержимое главы в структуре JSON
    try:
        chapter_data = json_data['props']['pageProps']['serie']['chapter']['title']
        content = f"Chapter title: {chapter_data}\n\n"
        
        chapter_body = json_data['props']['pageProps']['serie']['chapter_data']['data']['body']
        content += '\n'.join(chapter_body)
    except KeyError as e:
        print(f"Error extracting chapter content: {e}")
        print("JSON structure:")
        print(json.dumps(json_data, indent=2))
        return None
    
    return content

def save_chapter_to_api(chapter_number, content):
    print(f"Saving chapter {content} to API...")
    data = {
        "ranobe_id": RANOBE_ID,
        "chapter_number": chapter_number,
        "content_ru": "",
        "content_en": content,
        "content_cn": ""
    }
    
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 201:
        print(f"Successfully saved chapter {chapter_number}")
    else:
        print(f"Failed to save chapter {chapter_number}. Status code: {response.status_code}")
        print(f"Response: {response.text}")

def main():
    for i in range(NUM_CHAPTERS):
        chapter_number = START_CHAPTER + i
        print(f"Fetching chapter {chapter_number}...")
        content = fetch_chapter_content(chapter_number)
        if content:
            save_chapter_to_api(chapter_number, content)
        print("------------------------")

if __name__ == "__main__":
    main()
