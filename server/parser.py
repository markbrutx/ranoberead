import requests
from bs4 import BeautifulSoup
import json
import re

# Parser settings
BASE_URL = "https://wtr-lab.com/en/serie-619/losing-money-to-be-a-tycoon/chapter-{}"
START_CHAPTER = 747
NUM_CHAPTERS = 103
RANOBE_ID = 1  # ID of the existing ranobe in the database

# URL of your API for creating a new chapter
API_URL = "http://127.0.0.1:3000/chapters/"  # Updated to match your Flask API endpoint

def fetch_chapter_content(chapter_number_origin):
    url = BASE_URL.format(chapter_number_origin)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch chapter {chapter_number_origin}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        print(f"Could not find JSON data for chapter {chapter_number_origin}")
        return None
    
    json_data = json.loads(script_tag.string)
    
    try:
        full_title = json_data['props']['pageProps']['serie']['chapter_data']['data']['title']
        
        chapter_id_match = re.match(r'Chapter (\d+)', full_title)
        if not chapter_id_match:
            print(f"Could not extract chapter ID from title: {full_title}")
            return None
        
        chapter_id = int(chapter_id_match.group(1))
        title_en = full_title.replace(f"Chapter {chapter_id}", "").strip()

        chapter_body = json_data['props']['pageProps']['serie']['chapter_data']['data']['body']
        content_en = '\n'.join(chapter_body)
        
        return {
            'chapter_id': chapter_id,
            'chapter_number_origin': chapter_number_origin,
            'title_en': title_en,
            'content_en': content_en
        }
    except KeyError as e:
        print(f"Error extracting chapter content: {e}")
        print("JSON structure:")
        print(json.dumps(json_data, indent=2))
        return None

def save_chapter_to_api(chapter_data):
    print(f"Saving chapter {chapter_data['chapter_number_origin']} to API...")
    
    data = {
        "ranobe_id": RANOBE_ID,
        "chapter_id": chapter_data['chapter_id'],
        "chapter_number_origin": chapter_data['chapter_number_origin'],
        "title_en": chapter_data['title_en'],
        "content_en": chapter_data['content_en']
    }
    
    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 201:
            print(f"Successfully saved/updated chapter {chapter_data['chapter_number_origin']}")
        else:
            print(f"Failed to save/update chapter {chapter_data['chapter_number_origin']}. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error occurred while saving chapter {chapter_data['chapter_number_origin']}: {e}")

def main():
    for i in range(NUM_CHAPTERS):
        chapter_number_origin = START_CHAPTER + i
        print(f"Fetching chapter {chapter_number_origin}...")
        chapter_data = fetch_chapter_content(chapter_number_origin)
        if chapter_data:
            save_chapter_to_api(chapter_data)
        print("------------------------")

if __name__ == "__main__":
    main()
