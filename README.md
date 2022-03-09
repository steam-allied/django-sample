---
page_type: sample
languages:
- python
- mysql
products:
- vs-code
- mysql

description: "Creating REST API with Python, Django and MySQL hosted in docker"
urlFragment: "django-sample"
---

# Creating REST API with Python, Django and MySQL

[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/azure-samples/azure-sql-db-django/blob/main/LICENSE)

The sample uses the [Django](https://www.djangoproject.com/) web framework and [Django Rest framework](https://www.django-rest-framework.org/) package to easily implement REST APIs.

## How to run this sample

Clone this repository:

```bash
git clone https://github.com/steam-allied/django-sample
```

Alternatively you can clone the code using Visual Studio Code as well.

- Open the folder location where you want to clone the code
- In Visual Studio Code, select Source Control > ... > Clone (or select View, Command Palette and enter Git:Clone), paste the [Git repository URL](https://github.com/steam-allied/django-sample.git), and then select Enter</>.

Once you have the code downloaded to your local computer. You should see folder structure as below:

```properties
azure-sql-db-django
 ┣ votingapi
 ┃ ┣ migrations
 ┃ ┣ admin.py
 ┃ ┣ apps.py
 ┃ ┣ models.py
 ┃ ┣ serializers.py
 ┃ ┣ tests.py
 ┃ ┣ urls.py
 ┃ ┣ views.py
 ┃ ┗ __init__.py
 ┣ django-sql-project
 ┃ ┣ asgi.py
 ┃ ┣ settings.py
 ┃ ┣ urls.py
 ┃ ┣ wsgi.py
 ┃ ┗ __init__.py
 ┣ LICENSE
 ┣ manage.py
 ┣ README.md
 ┗ requirements.txt
```
## Setup Docker Containers
Run docker-compose build
Run docker-compose -f docker-compose.yml up

This will setup two containers. The db service will be provisioned first while the web service will wait till it can successfully connect to db service on port 3306 
![image](https://user-images.githubusercontent.com/16245910/157485207-7608928e-85c9-4588-8d67-003c34a29bff.png)

## Grant Permissions to test user (or whatever user you have specified in settings.py)
connect to db container
```docker exec -it db /bin/sh```
connect to mysql instance
```mysql -u root -p ```
on mysql prompt, grant permissions to test user to create new databases. Note: This step is needed for successful execution of unit tests as unit tests create temporary databases
```grant all privileges on *.* to 'test'@'%';```

## Perform Migrations
connect to web container
```docker exec -it web /bin/sh```
execute migrate command
```python manage.py migrate```
create django superuser. (Note: This is the user which will have admin access on your django admin shell)
```python manage.py createsuperuser```

## Start Django Admin Shell
On your host browser, browse http://localhost:8000/admin/ to connect to web instance
This should open the default Django admin shell
Login using the super user you created above


# docker settings
docker compose is using mysql , make sure to match docker settings and settings.py have same configuration for DB.
