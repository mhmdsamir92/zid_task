## ZID Ship assessment task

### Installation
We use `Poetry` depedency management system. So you will just need to install Poetry using the following command 
```
curl -sSL https://install.python-poetry.org | python3 -
```
Then use the following command to install the project 
```
poetry init
```

### API Installation
To make use of the API you need to do the following.

1- Configure MySql database configurations in settings module.

2- Run the following command to migrate the database
```
poetry run python manage.py migrate
```

3- Run the following command to start the server
```
poetry run python manage.py runserver
```

4- The server will be up and running on 
```
http://localhost:8000
```

### Documentation
After running the server a swagger documentation will be available using the following url
```
http://127.0.0.1:8000/docs/
```