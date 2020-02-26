# Fido
Personal telegram bot

## Required files

**config.py**
authorId = 'your numeric tg id'
admins = ['id1', 'id2', ...]

**token.txt**
just token without quotes

## Run
```
pipenv install
pipenv run python main.py

```

or more direct

```
pipenv --python /usr/bin/python3 run python3 main.py
```
or with pm2 

```
pm2 start pm2.yml
```