import json
import sqlite3

def db_to_json(db_path, output_json):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем все таблицы из базы данных
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    db_data = {}

    # Проходим по каждой таблице
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        table_data = []
        for row in rows:
            table_data.append(dict(zip(columns, row)))

        db_data[table_name] = table_data

    # Записываем всё в JSON файл
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(db_data, json_file, ensure_ascii=False, indent=4)

    # Закрываем соединение
    conn.close()

    print(f"Данные успешно экспортированы в {output_json}")

# Использование
db_to_json(r'D:\pet\ranoberead\server\instance\ranobe.db', 'output.json')

