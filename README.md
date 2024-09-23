# Ranobe Reader

Это проект для чтения ранобэ с веб-интерфейсом и API-бэкендом.

## Требования

- Python 3.8+
- Node.js 14+
- npm 6+

## Установка

### Бэкенд (FastAPI)

1. Клонируйте репозиторий:

   ```
   git clone https://github.com/markbrutx/ranoberead
   cd ваш_репозиторий/server
   ```

2. Создайте и активируйте виртуальное окружение:

   На Windows:

   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

   На macOS и Linux:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:

   ```
   pip install -r requirements.txt
   ```

4. Запустите сервер FastAPI:

   ```
   uvicorn main:app --reload
   ```

   Сервер будет доступен по адресу http://localhost:8000

### Фронтенд (Next.js)

1. Перейдите в директорию фронтенда:

   ```
   cd ../frontend
   ```

2. Установите зависимости:

   ```
   npm install
   ```

3. Запустите сервер разработки Next.js:

   ```
   npm run dev
   ```

   Фронтенд будет доступен по адресу http://localhost:3000

## Использование

- Откройте http://localhost:3000 в вашем браузере для доступа к веб-интерфейсу.
- API-документация доступна по адресу http://localhost:8000/docs

## Разработка

### Активация виртуального окружения

Перед работой с бэкендом всегда активируйте виртуальное окружение:

На Windows:

```
.\venv\Scripts\activate
```

На macOS и Linux:

```
source venv/bin/activate
```

### Запуск сервера FastAPI

```
cd server
uvicorn main:app --reload
```

### Запуск сервера Next.js

```
cd frontend
npm run dev
```

## Развертывание

Инструкции по развертыванию на продакшен-сервере будут добавлены позже.

## Вклад в проект

Пожалуйста, убедитесь, что вы следуете стилю кода проекта и добавляете тесты для новых функций.

## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)
