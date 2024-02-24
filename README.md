# Django Next Auth

Welcome to Quote Forge, your go-to tool for seamlessly crafting and managing quotes for your business.
This backend is built using Django. Create, customize, and organize business quotes with ease.

## Getting Started

Be sure to set the environment variables for the backend before starting.
In a terminal window, run the backend development server:

```bash
cd project_folder
```

## Create a virtual environment

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

## Install dependencies

```bash
poetry install
```

or

```bash
 pip install -r requirements.txt
```

## Create db migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

## Start Development Server

```bash
python manage.py runserver
```

## Start Production Server

```bash
gunicorn core.wsgi:application
```
