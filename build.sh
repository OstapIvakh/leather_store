#!/usr/bin/env bash
# exit on error
set -o errexit

# Оновлюємо pip і встановлюємо залежності
python -m pip install --upgrade pip
pip install -r requirements.txt

# Створюємо папку static, якщо її немає, щоб Django не сварився
mkdir -p static

# Збираємо статичні файли
python manage.py collectstatic --no-input

# Запускаємо міграції
python manage.py migrate

python create_admin.py