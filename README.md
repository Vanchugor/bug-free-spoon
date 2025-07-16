# bug-free-spoon

## Установка зависимостей и запуск

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Примеры curl-запросов

### 1

Запрос:

```bash
curl -X POST "http://127.0.0.1:8000/reviews" \
-H "Content-Type: application/json" \
-d '{"text": "Люблю ваш продукт!"}'
```

Ответ:

```bash
{
  "id": 1,
  "text": "Люблю ваш продукт!",
  "sentiment": "positive",
  "created_at": "2025-06-10T12:00:00.123456"
}
```

### 2

Запрос:

```bash
curl "http://127.0.0.1:8000/reviews?sentiment=negative"
```

Ответ:

```bash
[{"id":2,"text":"Ненавижу ваш продукт!","sentiment":"negative","created_at":"2025-07-16T22:01:44.309418"}]
```

