# 🧵 Korol Leather Workshop

A full-featured e-commerce web application for a handmade leather goods store,  
built with Django and deployed on Render.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?logo=postgresql)
![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render)

🔗 **Live Demo:** [korol-leather-workshop.onrender.com](https://korol-leather-workshop.onrender.com)

---

## About the Project

This is a real-world e-commerce project built for an actual leather goods workshop.  
The owner receives instant Telegram notifications on every order — the app is  
designed to work as a production tool, not just a demo.

---

## Features

- 🛍️ Product catalog with category filtering, search, and sorting (price / date / name)
- 🛒 Session-based shopping cart (no login required)
- 📦 Order checkout with customer details form
- 📬 Telegram Bot notifications — instant order alerts sent to the shop owner
- 📧 Email confirmation to the customer after each order
- 🔐 Django Admin panel for managing products, categories, and orders
- 📄 Pagination on the product listing page
- 🚀 Deployed on Render with Gunicorn + WhiteNoise for static files

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django |
| Database | PostgreSQL (production), SQLite (development) |
| Frontend | Bootstrap 5, HTML/CSS |
| Server | Gunicorn |
| Static files | WhiteNoise |
| Notifications | Telegram Bot API |
| Email | Django SMTP backend |
| Deployment | Render |

---

## Project Structure

```
leather_store/
├── catalog/          # Main app: models, views, forms, cart logic
│   ├── models.py     # Product, Category, Order, OrderItem
│   ├── views.py      # All views: catalog, cart, checkout
│   ├── cart.py       # Session-based cart logic
│   ├── forms.py      # Order form, filter form
│   └── utils.py      # Telegram notification helper
├── config/           # Django project settings and URLs
├── templates/        # HTML templates
├── requirements.txt
├── render.yaml       # Render deployment config
└── build.sh          # Build script for Render
```

---

## Local Setup

```bash
git clone https://github.com/OstapIvakh/leather_store.git
cd leather_store

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env  # Fill in your values

python manage.py migrate
python manage.py runserver
```

---

## Environment Variables

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=your-database-url
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
```

---

## What I Learned

- Integrating third-party APIs (Telegram Bot, SMTP email) into a Django project
- Session-based cart logic without a database
- Configuring production deployment: Gunicorn, WhiteNoise, environment variables
- Working with PostgreSQL in production vs SQLite in development

---

## Author

**Ostap Ivakh** — Junior Python Developer / QA Engineer  
[GitHub](https://github.com/OstapIvakh) · [LinkedIn](#)
