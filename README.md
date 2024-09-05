# Test Product API

## Запуск сервера (можно запускать через любой ASGI-сервер, в проекте используется uvicorn)
```
poetry run uvicorn api.views:app --reload
```
## Создание базы данных
Необходимо открыть REPL оболочку Python с помощью poetry
```
poetry run python
```
Далее ввести следующие команды
```
from api.models import *
Base.metadata.create_all(db)
```
## Тестирование запросов
Доступна интерактивная оболочка Swagger по URL /docs
