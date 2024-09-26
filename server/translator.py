import requests
import os
import time
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Настройки
RANOBE_ID = 1
START_CHAPTER = 416
NUM_CHAPTERS = 3
API_URL = "http://192.168.0.165:3000/chapters"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_TOKENS = 4096
RETRY_DELAY = 15  # seconds

# Инициализация асинхронного клиента OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_chapter_content(ranobe_id, chapter_number):
    """Получение содержания главы с API"""
    print(f"Fetching content for chapter {chapter_number}...")
    try:
        response = requests.get(f"{API_URL}/{ranobe_id}/{chapter_number}")
        response.raise_for_status()
        data = response.json()
        content = data.get('content_en')
        title = data.get('title_en')
        print(f"Successfully fetched content for chapter {chapter_number}. Length: {len(content)} characters.")
        return content, title
    except requests.exceptions.RequestException as e:
        print(f"Error fetching chapter {chapter_number}: {e}")
        return None, None

def split_content(content, max_tokens=MAX_TOKENS):
    """Разделение содержания на части, не превышающие максимальное количество токенов"""
    words = content.split()
    parts = []
    current_part = []
    current_tokens = 0

    for word in words:
        word_tokens = len(word) // 4 + 1  # Грубая оценка количества токенов
        if current_tokens + word_tokens > max_tokens:
            parts.append(' '.join(current_part))
            current_part = [word]
            current_tokens = word_tokens
        else:
            current_part.append(word)
            current_tokens += word_tokens

    if current_part:
        parts.append(' '.join(current_part))

    print(f"Content split into {len(parts)} parts.")
    return parts

async def translate_part(part, part_number, total_parts):
    """Перевод части содержания с использованием GPT-4o через асинхронный клиент OpenAI"""
    prompt = (
        "переведи на русский и пожалуйста сохраняй стиль нормального повествования и пунктуацию\n\n"
        "а не делай тупой машинный перевод\n\nесли че там босс Пэй именно\n\n" + part
    )

    print(f"Translating part {part_number}/{total_parts}. Length: {len(part)} characters.")
    
    attempt = 1
    while True:
        try:
            completion = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Вы - профессиональный переводчик с английского на русский который умеет по смыслу адаптировать текст в читабельном виде и устроняет машинный перевод в угоду человекоподобному адаптивному переводу."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=MAX_TOKENS
            )
            translated = completion.choices[0].message.content.strip()
            print(f"Successfully translated part {part_number}/{total_parts}. Translated length: {len(translated)} characters.")
            return translated
        except Exception as e:
            print(f"Error during translation of part {part_number}/{total_parts} (Attempt {attempt}): {e}")
            if "rate_limit" in str(e).lower():
                print(f"Rate limit reached. Retrying in {RETRY_DELAY} seconds...")
                await asyncio.sleep(RETRY_DELAY)
                attempt += 1
            else:
                return None

async def translate_content(content):
    """Разделение содержания на части, последовательный перевод частей и объединение результатов"""
    parts = split_content(content)
    translated_parts = []
    for i, part in enumerate(parts, 1):
        translated_part = await translate_part(part, i, len(parts))
        if translated_part:
            translated_parts.append(translated_part)
        else:
            print(f"Failed to translate part {i}/{len(parts)}. Skipping...")
        if i < len(parts):
            print(f"Waiting 1 second before translating the next part...")
            await asyncio.sleep(1)  # Небольшая задержка между запросами
    
    full_translation = " ".join(translated_parts)
    print(f"Full translation completed. Total length: {len(full_translation)} characters.")
    return full_translation

async def translate_title(title):
    """Перевод заголовка главы на русский"""
    prompt = f"Переведи на русский заголовок: {title}"
    print(f"Translating title: {title}")
    
    try:
        completion = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Вы - профессиональный переводчик с английского на русский который умеет по смыслу адаптировать текст в читабельном виде."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100  # Небольшой лимит для перевода заголовка
        )
        translated_title = completion.choices[0].message.content.strip()
        print(f"Successfully translated title. Translated title: {translated_title}")
        return translated_title
    except Exception as e:
        print(f"Error translating title: {e}")
        return None

def update_translation(ranobe_id, chapter_number, translated_content, translated_title=None):
    """Обновление перевода главы на сервере"""
    print(f"Updating translation for chapter {chapter_number}...")
    data = {"content_ru": translated_content}
    if translated_title:
        data["title_ru"] = translated_title

    try:
        response = requests.put(
            f"{API_URL}/{ranobe_id}/{chapter_number}/update_translation",
            json=data
        )
        response.raise_for_status()
        print(f"Successfully updated translation for chapter {chapter_number}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating chapter {chapter_number}: {e}")

async def process_chapter(ranobe_id, chapter_number):
    """Обработка одной главы"""
    print(f"Starting to process chapter {chapter_number}...")
    content, title = await get_chapter_content(ranobe_id, chapter_number)
    if content:
        print(f"Starting translation of chapter {chapter_number}...")
        translated_content = await translate_content(content)
        translated_title = await translate_title(title)
        if translated_content:
            print(f"Translation of chapter {chapter_number} completed. Updating on server...")
            update_translation(ranobe_id, chapter_number, translated_content, translated_title)
        else:
            print(f"Failed to translate chapter {chapter_number}. Skipping update...")
    else:
        print(f"No content found for chapter {chapter_number}. Skipping...")
    print(f"Finished processing chapter {chapter_number}")
    print("------------------------")

async def main():
    """Основная асинхронная функция, последовательно обрабатывающая главы"""
    for i in range(NUM_CHAPTERS):
        chapter_number = START_CHAPTER + i
        await process_chapter(RANOBE_ID, chapter_number)
        if i < NUM_CHAPTERS - 1:
            print(f"Waiting 5 seconds before processing the next chapter...")
            await asyncio.sleep(5)  # Задержка между обработкой глав
    print("All chapters processed. Script execution completed.")

if __name__ == "__main__":
    asyncio.run(main())
