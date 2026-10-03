# ShopEase — CodeAlpha Full Stack E-commerce

A dynamic e-commerce internship project built with Django, SQLite, HTML, CSS and JavaScript.

## Features
- Dynamic product catalog from database
- Search and category filtering
- Product detail pages
- User registration and login
- Session-based shopping cart
- Quantity update/remove
- Dynamic cart totals
- Checkout and order creation
- My Orders page
- Django admin for products and orders
- Responsive premium UI

## Run
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/
