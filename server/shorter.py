import json

def compress_json(input_file, output_file):
    # Читаем исходный JSON файл
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Рекурсивная функция для обработки данных
    def compress_data(item):
        if isinstance(item, dict):
            return {key: compress_data(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [compress_data(elem) for elem in item[:2]]  # Оставляем максимум два элемента
        elif isinstance(item, str):
            return item[:100]  # Обрезаем строки до 100 символов
        else:
            return item

    # Применяем сжатие данных
    compressed_data = compress_data(data)

    # Записываем результат в новый JSON файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compressed_data, f, ensure_ascii=False, indent=4)

    print(f"Сжатый JSON сохранён в {output_file}")

# Использование
compress_json(r'D:\pet\ranoberead\server\output.json', r'D:\pet\ranoberead\server\mock_output.json')
