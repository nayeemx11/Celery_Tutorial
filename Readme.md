# This document is for the Celery working with Django, using RabbitMQ as Massage Broker

## Settings up `Django` for `Celery`

- Django
    - Setting up Celery within Django
    ```sh
    pip install celery
    ```
    - Add this in the project level directory by creating a file `celery.py` named and contents will be:

        ```py
        # celery.py
        import os
        from celery import Celery

        # Set the default Django settings module for the 'celery' program.
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_tutorial.settings')

        app = Celery('celery_tutorial')

        # Using a string here means the worker doesn't have to serialize
        # the configuration object to child processes.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.
        app.config_from_object('django.conf:settings', namespace='CELERY')

        # Load task modules from all registered Django apps.
        app.autodiscover_tasks()
        ```

    - replace the placeholder `project_name` by appropiate name of your Django project name in my case it is `celery_tutorial`

        ```py
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', '[project_name].settings')
        ``` 
        ```py
        app = Celery('[project_name]')
        ```

below porstion will be in a new django-app
- Add tasks for celery

    ```py
    # tasks.py
    from celery import shared_task

    @shared_task
    def add(x, y):
        return x + y

    @shared_task
    def every_10_s():
        return 10
    ```

- Setup `view.py` for calling the tasks
    ```py
    # views.py
    from django.shortcuts import render

    from django.http import HttpResponse
    from .tasks import add

    def my_view(request):
        result = add.apply_async(args=[10, 20])  # Call task asynchronously
        return HttpResponse(f"Task result: {result.id}")
    ```
    task must be call with `apply_async(args*)` or `deley()`

- corresponding `urls.py` file in response
    ```py
    # urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.my_view, name="home"),
    ]
    ```
## Setting up `RabbitMQ` for `Celery`

- Install `Erlang` (a dependency of `RabbitMQ`)
    - Install `erlang` before RabbitMQ `https://www.erlang.org/`
    - Instal RabbitMQ `https://www.rabbitmq.com/`
    - Enable RabbitMQ Management Plugin
        ```sh
        rabbitmq-plugins enable rabbitmq_management
        ```
    - setup this lines in `settings.py` 

        ```py
        # building connection the rabbitQ
        CELERY_BROKER_URL = 'amqp://localhost' 
        # Storing result
        CELERY_RESULT_BACKEND = 'rpc://'
        CELERY_TIMEZONE = 'UTC'
        # for API
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        ```

    because this is locally running so the `CELERY_BROKER_URL` is allocate to localhost
    - now start the RabbitMQ server application for star-menu in case of windows

## Celery setup is complete

### setup Celery-Beat for the schedule task


### Now power-up three different terminal for tracking your work
- for the schedule task install celery-beat
    ```sh
    pip install django-celery-beat
    ```

- add this line in `INSTALLED_APPS`
    ```py
    'django_celery_beat',
    ```

- add this code snippets in settings.py
    ```py
    CELERY_BEAT_SCHEDULE = {
        "every_10_seconds":{
            "task": "polls.tasks.every_10_s",
            "schedule": 10, # every 10 seconds
        },
    }
    ```
    here `task` and `schedule` are not optional
    - `task` is for specification what method will be in schedule task
    - `schedule` is for the time, here I have set it to 10 seconds

## Now Comes the running section
- for the worker
```sh
celery -A celery_tutorial worker --pool=solo -l info
```

- for the django running
```sh
python manage.py runserver
```

- for the celery-beat
```sh
celery -A celery_tutorial beat -l info
```

## RabiitMQ
- start RabbitMQ service
- `http://localhost:15672`

