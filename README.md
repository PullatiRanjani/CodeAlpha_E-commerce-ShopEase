🛍️ CodeAlpha Ecommerce – ShopEase

ShopEase is a dynamic full-stack e-commerce web application developed as part of the CodeAlpha Full Stack Development Internship.

The application provides a user-friendly online shopping experience where customers can browse products, view product details, manage their cart, place orders, and submit reviews and ratings.

🚀 Features

- 🏠 Attractive and responsive e-commerce interface
- 👗 Fashion and fashion accessories categories
- 🔍 Product browsing and product details
- 🛒 Add products to cart
- ➕➖ Increase or decrease cart quantity
- 📦 Place orders
- ⭐ Customer ratings and reviews
- 👨‍💼 Django admin panel for managing:
  - Products
  - Categories
  - Orders
  - Reviews
- 🔄 Live order monitoring
- 📱 Responsive design for different screen sizes

🛠️ Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Django
- Database: SQLite
- Programming Language: Python
- Version Control: Git & GitHub

📂 Project Structure

CodeAlpha_Ecommerce/
│
├── manage.py
├── requirements.txt
│
├── store/
│   ├── views.py
│   ├── models.py
│   ├── admin.py
│   ├── migrations/
│   └── management/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── admin/
│   └── HTML templates
│
└── shopease/
    ├── settings.py
    ├── urls.py
    ├── middleware.py
    ├── asgi.py
    ├── wsgi.py
    └── __init__.py

⚙️ Installation & Setup

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/CodeAlpha_Ecommerce.git
cd CodeAlpha_Ecommerce

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows:

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Run migrations

python manage.py migrate

6. Start the development server

python manage.py runserver

Open the application in your browser:

http://127.0.0.1:8000/

👨‍💼 Admin Panel

The Django admin panel can be used to manage products, categories, orders, and customer reviews.

http://127.0.0.1:8000/admin/

Create an admin account using:

python manage.py createsuperuser

🎯 Project Objective

The main objective of ShopEase is to create a practical and dynamic e-commerce platform that provides customers with a simple shopping experience while allowing administrators to efficiently manage products, orders, and reviews.

💡 Future Enhancements

- Online payment integration
- Customer authentication and profiles
- Order tracking
- Wishlist functionality
- Product search and advanced filtering
- Email notifications
- Deployment with a production database

👩‍💻 Developed For

CodeAlpha Full Stack Development Internship

Project

CodeAlpha Ecommerce – ShopEase

---

⭐ If you find this project useful, feel free to explore the repository and try the application.
