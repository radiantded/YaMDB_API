# YaMDB API
Проект собирает отзывы пользователей на произведения. Произведения делятся на категории и жанры, а также имеют рейтинг, основанный на оценках пользователей.

## Стек технологий
Python 3.9.4, Django 3.1+, Django REST Framework, SQLite3, Simple JWT, Django Filter.

## Установка
Установите зависимости в виртуальном окружении: 
```bash
pip install -r requirements.txt
```
В корневой директории создайте файл "```.env```" со следующим кодом:
```
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
DEBUG=False
ALLOWED_HOSTS=*
```
Перез запуском убедитесь, что применили все миграции:
```bash
python manage.py migrate
python manage.py runserver
```

## Импорт информации в базу данных
Импортируйте и запустите скрипт используя Python shell:
```python
from data.import_data import import_data
import_data()
```

## Импорт информации из csv файла
Импортируйте необходимые модели и скрипт используя Python shell:
```python
from api.models import User, Category, Comment, Genre, Review, Title
from data.import_data import create_models
```
Запустите скрипт со следующими параметрами:

```file_path``` — путь до вашего csv файла,

```model``` — класс модели из импортированных ранее,

Пример:
```python
create_models('data/review.csv', Review)
```

## Авторизация
От имени суперпользователя отправьте POST-запрос с указанием email на адрес: ```http://127.0.0.1:8000/api/v1/auth/email/```
Пример:
```bash
curl -X POST -F "email=ваша_почта@gmail.com" http://127.0.0.1:8000/api/v1/auth/email/
```
Эмулятор почтового сервера создаст файл-письмо с кодом авторизации в папке ```./sent_emails/```.

Для получения токена отправьте POST-запрос с кодом авторизации на ```http://127.0.0.1:8000/api/v1/auth/token/```.
Пример:
```bash
curl -X POST -F "email=ваша_почта@gmail.com" -F "confirmation_code=ваш_код" http://127.0.0.1:8000/api/v1/auth/token/
```

## Документация
Документация проекта доступна по следующей ссылке:
```http://127.0.0.1:8000/redoc/```
