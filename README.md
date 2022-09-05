# Проектная работа 7 спринта

Ссылка на репозиторий Async Cinema https://github.com/IAmIrina/Async_API_sprint_2.git, в котором реализован Middleware с проверкой прав пользователя в Auth.

## Сервис авторизации

Предназначен для регистрации пользователей и управлением ролями пользователей.

## Используемые технологии
Протокол REST API.
Код приложения на Python + Flask.
Приложение запускается под управлением сервера ASGI(guvicorn).
В качестве хранилища используется PostgreSQL.
Для кеширования используется Redis.
Для функционального тестирования используется pytest.
Подключен Jaeger.
Реализован Docker для запуска.

Компоненты системы: Postgress, Redis, Nginx, Jaeger, Docker-Compose.

Доп.инфо: реализован троттлинг и партицирование для таблицы входов.

#Сервис авторизации

## Ссылка на репозиторий

[Репозиторий Сервис авторизации](https://github.com/alexshvedov1997/Auth_sprint_2.git)

## Внешняя Swager Документация

[Swagger](http://127.0.0.1/apidocs)

## Style guide
Минимум, который необходимо соблюдать:
- [PEP8](https://peps.python.org/pep-0008/)  +  [Google Style Guide](https://google.github.io/styleguide/pyguide.html)


## Инструкция по разворачиванию сервиса

Склонировать репозиторий
```
git clone https://github.com/alexshvedov1997/Auth_sprint_1.git
```
Скопировать файл:  
```
cp .env.example .env
```
Отредактировать переменные окружения в файле .env любимым редактором. 

### Развернуть сервис в режиме DEV

В режими DEV:
- API под управлением встроенное сервера Flask.
- Миграция базы данных.

```
sudo make dev
```

### Развернуть сервис в режиме PROD
В режими DEV запускается API под управлением Guvicorn с патчем для асинхронки.

```
sudo make up
```
или в detach режиме
```
sudo make up_detach
```

### Запустить тесты
```
sudo make test
```

### Команда на создание суперпользователя


Пример комманды
flask create_superuser <str: login> <str: password> <str: email>

flask create_superuser Tom hollabd holland@mail.ru

Запускать команду из папки где app.py


