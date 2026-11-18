# Library API

Небольшой REST API для управления библиотекой. Можно добавлять авторов и книги, получать списки, обновлять и удалять записи. Все данные лежат в PostgreSQL.

Проект написан на чистом SQL через psycopg2, без SQLAlchemy и Alembic. Хотелось разобраться как FastAPI работает с базой напрямую, без ORM-прослойки.

## Стек

- Python 3.12
- FastAPI
- PostgreSQL
- psycopg2-binary
- uvicorn
- Pydantic v2
- python-dotenv

## Структура

~~~
fastapi-library-api/
├── app/
│   ├── main.py          # приложение и роуты
│   ├── db.py            # подключение к базе
│   └── schemas.py       # pydantic-модели
├── database/
│   └── schema.sql       # создание таблиц и начальные данные
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
~~~

## Что нужно для запуска

- Python 3.10 или новее
- PostgreSQL (должен быть установлен и запущен)
- DBeaver или любой другой клиент для PostgreSQL (по желанию)

## Установка

Клонируешь репозиторий и заходишь в папку:

~~~bash
git clone https://github.com/piero4325/fastapi-library-api.git
cd fastapi-library-api
~~~

Создаёшь виртуальное окружение:

~~~bash
python -m venv venv
~~~

Активируешь его. На Windows:

~~~bash
venv\Scripts\activate
~~~

На Linux/Mac:

~~~bash
source venv/bin/activate
~~~

Ставишь зависимости:

~~~bash
pip install -r requirements.txt
~~~

## Настройка базы данных

Создай базу данных в PostgreSQL. Например через DBeaver или psql:

~~~sql
CREATE DATABASE library_db;
~~~

Потом выполни файл `database/schema.sql` — он создаст таблицы authors и books и заполнит их начальными данными. В DBeaver это делается через File → Open File → выбрать schema.sql → Execute Script (Alt+X).

## Переменные окружения

Скопируй `.env.example` в `.env`:

~~~bash
copy .env.example .env
~~~

На Linux/Mac:

~~~bash
cp .env.example .env
~~~

Открой `.env` и впиши свои данные для подключения к PostgreSQL:

~~~
DB_HOST=localhost
DB_PORT=5432
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=твой_пароль
~~~

Файл `.env` не попадает в git, он в `.gitignore`.

## Запуск

~~~bash
uvicorn app.main:app --reload
~~~

Сервер поднимется на http://127.0.0.1:8000

Swagger UI доступен по адресу http://127.0.0.1:8000/docs — там можно потестить все эндпоинты прямо из браузера.

## API эндпоинты

### Авторы

| Метод | Путь | Описание |
|-------|------|----------|
| GET | /authors | Получить всех авторов |
| POST | /authors | Создать автора |

### Книги

| Метод | Путь | Описание |
|-------|------|----------|
| GET | /books | Получить все книги |
| POST | /books | Создать книгу |
| PUT | /books/{id} | Обновить книгу |
| DELETE | /books/{id} | Удалить книгу |

## Примеры запросов

Создать автора:

~~~json
POST /authors
{
  "name": "Stephen King",
  "country": "USA"
}
~~~

Создать книгу:

~~~json
POST /books
{
  "title": "The Shining",
  "year": 1977,
  "author_id": 6
}
~~~

Обновить книгу:

~~~json
PUT /books/1
{
  "title": "Crime and Punishment (Updated)",
  "year": 1866,
  "author_id": 1
}
~~~

## Валидация

Год книги не может быть больше текущего года и не может быть меньше 1000. Если передать невалидные данные — FastAPI вернёт 422 с описанием ошибки.

Если указать author_id которого нет в базе — PostgreSQL вернёт ошибку внешнего ключа.

## База данных

Две таблицы со связью один-ко-многим:

- authors (id, name, country)
- books (id, title, year, author_id)

author_id в books ссылается на id в authors через FOREIGN KEY. При попытке удалить автора у которого есть книги — PostgreSQL не даст это сделать.

## Что можно улучшить

- Добавить пагинацию для списков
- Добавить фильтрацию книг по автору или году
- Подключить SQLAlchemy и Alembic для миграций
- Добавить тесты
- Добавить аутентификацию