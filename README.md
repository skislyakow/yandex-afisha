# Куда пойти — Москва глазами Артёма

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django)](https://www.djangoproject.com/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.6-199900?logo=leaflet)](https://leafletjs.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-2-4FC08D?logo=vuedotjs)](https://vuejs.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4-7952B3?logo=bootstrap)](https://getbootstrap.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![dvmn](https://img.shields.io/badge/Проект-dvmn.org-FF6600)](https://dvmn.org)

Интерактивная карта интересных мест Москвы. Проект создан в рамках обучения на [Devman](https://dvmn.org).

## Возможности

- Интерактивная карта Москвы с метками интересных мест
- Детальная информация о каждом месте: описание, фотографии
- WYSIWYG-редактор для удобного наполнения контента
- Админ-панель с drag-and-drop сортировкой фотографий
- JSON API для получения данных о местах

## Требования

- Python 3.12+
- Django 6.0
- SQLite (разработка) / PostgreSQL (продакшн)

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd yandex-afisha
```

### 2. Создать и активировать виртуальное окружение

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

Если файла `requirements.txt` ещё нет, установите пакеты вручную:

```bash
pip install django==6.0 django-tinymce django-admin-sortable2 environs
```

### 4. Настроить переменные окружения

Скопируйте файл `.env.example` в `.env` и отредактируйте:

```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
```

Содержимое `.env`:

```ini
SECRET_KEY=django-insecure-ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

| Переменная | Обязательно | Описание |
|-----------|-------------|----------|
| `SECRET_KEY` | Да | Секретный ключ Django |
| `DEBUG` | Нет | Режим отладки (`True`/`False`). По умолчанию `False` |
| `ALLOWED_HOSTS` | Нет | Список хостов через запятую. По умолчанию пусто |

### 5. Выполнить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

### Загрузка данных о местах

Для наполнения базы данных используйте management-команду `load_place`:

```bash
python manage.py load_place <url>
```

Команда принимает два формата ссылок:

- Обычная ссылка с GitHub (автоконвертируется):
  ```
  https://github.com/.../blob/master/places/Название.json
  ```
- Прямая ссылка на сырой JSON:
  ```
  https://raw.githubusercontent.com/.../master/places/Название.json
  ```

Команда скачивает JSON, создаёт или обновляет место и загружает фотографии.

Ожидаемый формат входного JSON:

```json
{
    "title": "Название места",
    "description_short": "Короткое описание...",
    "description_long": "<p>Полное описание с HTML...</p>",
    "coordinates": {
        "lng": "37.64912239999976",
        "lat": "55.77754550000014"
    },
    "imgs": [
        "https://raw.githubusercontent.com/.../photo1.jpg",
        "https://raw.githubusercontent.com/.../photo2.jpg"
    ]
}
```

## Использование

### Админ-панель

1. Зайдите на http://127.0.0.1:8000/admin/
2. Добавьте места через раздел **Places**
3. Для каждого места можно загрузить фотографии и отсортировать их drag-and-drop
4. Поле с длинным описанием оборудовано WYSIWYG-редактором

### API

- `GET /places/<id>/` — JSON с данными о месте

Пример ответа:

```json
{
    "title": "Экскурсионная компания «Легенды Москвы»",
    "imgs": ["/media/places_images/photo.jpg"],
    "description_short": "Короткое описание...",
    "description_long": "<p>Полное описание с HTML...</p>",
    "coordinates": {
        "lng": "37.64912239999976",
        "lat": "55.77754550000014"
    }
}
```

## Деплой

### 1. Настроить переменные окружения на сервере

```ini
SECRET_KEY=<надёжный-секретный-ключ>
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
```

### 2. Собрать статику

```bash
python manage.py collectstatic
```

### 3. Настроить базу данных

Для продакшна рекомендуется PostgreSQL. Настройте соединение через переменные окружения:

```python
# settings.py (пример)
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}
```

### 4. Запустить через WSGI-сервер

Пример настройки для Gunicorn:

```bash
gunicorn where_to_go.wsgi:application
```

### 5. Настроить веб-сервер

Пример для Nginx:

```nginx
location /static/ {
    alias /path/to/staticfiles/;
}

location /media/ {
    alias /path/to/media/;
}

location / {
    proxy_pass http://127.0.0.1:8000;
}
```

## Структура проекта

```
yandex-afisha/
├── manage.py
├── .env                    # Переменные окружения (не в git)
├── .env.example            # Пример переменных окружения
├── .gitignore
├── README.md
├── requirements.txt
├── media/                  # Загруженные файлы (не в git)
├── static/                 # Статические файлы
│   ├── favicon.png
│   ├── hand-pointer-regular.svg
│   ├── leaflet-sidebar.css
│   └── leaflet-sidebar.js
├── templates/
│   └── index.html          # Главная страница с картой
├── places/                 # Приложение Places
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── migrations/
└── where_to_go/            # Конфигурация Django
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Технологии

- **Django 6.0** — веб-фреймворк
- **django-tinymce** — WYSIWYG-редактор
- **django-admin-sortable2** — drag-and-drop сортировка в админке
- **Leaflet.js** — интерактивная карта
- **Vue.js 2** — реактивный интерфейс
- **environs** — управление переменными окружения

## Учебный проект

Данный проект создан в рамках курса [Devman](https://dvmn.org) для изучения Django.

## Лицензия

Проект распространяется под лицензией MIT. Подробнее — в файле [LICENSE](LICENSE).
