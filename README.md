## Introduction
This project is built base on [Django](https://www.djangoproject.com/) and [django-rest-framework](http://www.django-rest-framework.org/) with Python 3.6+

* Django for routing and modeling database
* django-rest-framework for handling request and response data

## Setup development environment
### Requirements

* Python 3.6+
* All libraries in `requirements-lock.txt`
* PostgresSQL server
* Docker (for test and local dev)

## Coding style

**This project uses [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style**. So, when working on this project, you should follow to this style as much as possible. We suggest using [black](https://github.com/psf/black) as code formatter.

## Swagger

**This project use [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) for Swagger generator.**

## Unittest

Sample command:

```bash
python manage.py test --verbosity=3 apps.sessions.tests
```
