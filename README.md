# Project work: "Authorization for Online Cinema.".


[Repository Async Search Cinema](https://github.com/IAmIrina/Async_API_sprint_2.git) which implements middleware to check users roles in this authorization service.


## Auhorization service


Designed for user registration and user role management.


## Applied technology
- Protocol REST API
- Python + Flask
- ASGI(guvicorn)
- PostgreSQL as user data storage
- Redis as cache
- pytest
- Jaeger
- Docker


Components: Postgres, Redis, Nginx, Jaeger, Docker-Compose.


Implement throtling and partitions for the logging table.



##  Swager documentation


[Swagger](http://127.0.0.1/apidocs)


## Style guide
- [PEP8](https://peps.python.org/pep-0008/)  +  [Google Style Guide](https://google.github.io/styleguide/pyguide.html)



## How to deploy service


Clone repository:
```
git clone https://github.com/alexshvedov1997/Auth_sprint_1.git
```
Copy file:  
```
cp .env.example .env
```
Set your environment variables in .env file with any editor.


### Deploy in DEV mode.


DEV mode:
- API starts under the internal Flask service.
- Database migration.


```
sudo make dev
```


### Deploy in PROD mode
API starts under the Gunicorn server with an async patch in PROD mode.


```
sudo make up
```
or detach mode
```
sudo make up_detach
```


### Run tests
```
sudo make test
```


### Command to create a superuser


Example:
flask create_superuser <str: login> <str: password> <str: email>


flask create_superuser Tom Holland holland@mail.ru


Run the command in a folder that contains app.py file
