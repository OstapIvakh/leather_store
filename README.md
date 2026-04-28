🧵 Korol Leather Workshop
A full-featured e-commerce web application for a handmade leather goods store, built with Django and deployed on Render.
🔗 Live Demo: korol-leather-workshop.onrender.com

Features

🛍️ Product catalog with category filtering, search, and sorting (by price, date, name)
🛒 Shopping cart powered by Django sessions
📦 Order checkout with customer details form
📬 Telegram bot notifications — instant order alerts with full details sent to the shop owner
📧 Email confirmation sent to the customer after each order
🔐 Django Admin panel for managing products, categories, and orders
📄 Pagination on the product listing page
🚀 Deployed on Render with Gunicorn and static files via WhiteNoise


Tech Stack
LayerTechnologyBackendPython 3, DjangoDatabasePostgreSQL (production), SQLite (development)ServerGunicornStatic filesWhiteNoiseNotificationsTelegram Bot APIEmailDjango email backend (SMTP)DeploymentRender

Project Structure
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

Local Setup
bash# Clone the repository
git clone https://github.com/OstapIvakh/leather_store.git
cd leather_store

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver

Environment Variables
Create a .env file in the root directory with the following variables:
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=your-database-url
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com

Author
Ostap Ivakh — Junior Python Developer
GitHub