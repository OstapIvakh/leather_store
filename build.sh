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

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'ostap@example.com', 'very_complicated_password_123')
else:
    u = User.objects.get(username='admin')
    u.set_password('very_complicated_password_123')
    u.save()
    print('Password reset')
print('Done')
"