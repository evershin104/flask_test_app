# Запуск

Требуется `poetry == 2.1.3`, `python >= 3.13`.

Команды запуска - 
```shell
poetry shell

poetry install

# Из под окружения
python run.py

# Или 
poetry run python run.py
```

Если БД есть - применятся новые миграции, иначе - создаст БД и применит миграции.


## Файловая структура проекта

```shell
.
├── README.md
├── app                     - Можно использовать как хранилище 
│   │                       - приложений, но тут приложение с reviews одно
│   ├── __init__.py
│   ├── api                 - Директория с роутами приложения
│   │   ├── __init__.py
│   │   └── review_api.py   - Хэндлеры запросов
│   ├── config.py
│   ├── models.py
│   ├── routes.py           - Здесь только регистрирует вьюшки приложения
│   └── schema.py           - Сериализация
├── instance                - Тут БД создаваться будет
│   └── test.db
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 3149d2b9e0f5_add_manual_index_on_created_ad.py          - Создали индекс на дату
│       ├── 6c3dd67a6319_create_reviews_table.py                    - Создали таблицы
│       └── 8b892e7403cd_add_manual_index_on_sentiment_and_.py      - Сделали составной индекс на поиск
├── poetry.lock
├── pyproject.toml
└── run.py                  - Это запускаем
```
Вообще хотелось что-то flexible сделать, чтобы в `api` собирать вьюхи, ставить им в `api/__init__.py` им 
префикс, например `v1/...`, а в роутах уже добавлять `api/..`, чтобы получать
адекватное версионирование API и обеспечение обратной совместимости со старыми API при выпуске новой версии.

Индексов в БД для красоты еще добавил :)

## Примеры использования API [POST]

### 201 Created
```shell
Endpoint - http://127.0.0.1:5000/api/v1/reviews
Body: {"text": "плохо"}

curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "хорошо"}'


Response:
{
	"created_at": "2025-07-09T19:51:25.346658",
	"id": 60,
	"sentiment": "negative",
	"text": "плохо"
}
```

### 422 Unprocessable entity 
```shell
Endpoint - http://127.0.0.1:5000/api/v1/reviews
Body: {"not_text": "плохо"}

curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "хорошо"}'


Response:
{
	"code": 422,
	"errors": {
		"json": {
			"not_text": [
				"Unknown field."
			],
			"text": [
				"Missing data for required field."
			]
		}
	},
	"status": "Unprocessable Entity"
}
```
или
```shell
Endpoint - http://127.0.0.1:5000/api/v1/reviews
Body: {"not_text": "плохо"}

curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "хорошо"}'


Response:
{
	"code": 422,
	"errors": {
		"json": {
			"not_text": [
				"Unknown field."
			]
		}
	},
	"status": "Unprocessable Entity"
}
```

## Примеры использования API [GET]
Есть пагинация по 10 элементов на страницу.
### 200 Ok
```shell
Endpoint - http://127.0.0.1:5000/api/v1/reviews
Body: {"text": "плохо"}

curl -X GET "http://127.0.0.1:5000/api/v1/reviews?sentiment=positive"



Response:
[
	{
		"created_at": "2025-07-09T20:05:20.784557",
		"id": 61,
		"sentiment": "negative",
		"text": "плохо"
	},
	{
		"created_at": "2025-07-09T19:51:25.346658",
		"id": 60,
		"sentiment": "negative",
		"text": "плохо"
	},
	....
]
```

### 200 Ok, фильтрация (sentiment only)
```shell
Endpoint - http://127.0.0.1:5000/api/v1/reviews?sentiment=positive
Body: {"text": "плохо"}

curl -X GET "http://127.0.0.1:5000/api/v1/reviews"



Response:
[
	{
		"created_at": "2025-07-09T19:51:21.200214",
		"id": 44,
		"sentiment": "positive",
		"text": "хорошо"
	},
	{
		"created_at": "2025-07-09T19:51:21.117237",
		"id": 43,
		"sentiment": "positive",
		"text": "хорошо"
	},
	...
]
```

### 200 Ok, фильтрация + страницы (sentiment only)
```shell
Endpoint - http://127.0.0.1:5000/api/v1/reviews?sentiment=positive&page=2
Body: {"text": "плохо"}

curl -X GET "http://127.0.0.1:5000/api/v1/reviews"



Response:
[
	{
		"created_at": "2025-07-09T19:51:19.915842",
		"id": 34,
		"sentiment": "positive",
		"text": "хорошо"
	},
	{
		"created_at": "2025-07-09T19:51:19.815010",
		"id": 33,
		"sentiment": "positive",
		"text": "хорошо"
	},
	...
]
```



