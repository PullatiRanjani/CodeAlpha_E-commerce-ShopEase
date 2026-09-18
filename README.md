#**ShopEase – E-Commerce Website**

An application where you explore products, shop online, manage your cart, place orders, and share your reviews.

ShopEase is a full-stack e-commerce web application developed as part of the CodeAlpha Full Stack Development Internship.

It provides a simple and interactive platform where users can browse products, explore categories, add products to their cart, place orders, and share ratings and reviews. The application also includes an admin panel for managing products, categories, orders, and reviews.

##**🚀 Features**

**🛍️ Product Browsing**

- Browse available products
- Explore products by categories
- View product details
- Display product prices and ratings
- Dynamic product management

**🛒 Shopping Cart**

- Add products to cart
- Increase and decrease product quantity
- Remove products from cart
- View cart items and total price
- Manage cart dynamically

**📦 Orders**

- Place orders from the shopping cart
- Store order details in the database
- View and manage orders
- Admin order management

**⭐ Reviews & Ratings**

- Customers can submit product reviews
- Customers can provide ratings
- View ratings and reviews for products
- Admin can manage customer reviews

**👨‍💼 Admin Panel**

- Manage products
- Manage product categories
- Manage orders
- Manage customer reviews
- Monitor incoming orders
- Live order monitoring

**📱 Responsive Design**

- Desktop-friendly interface
- Mobile-friendly layout
- Responsive navigation
- Clean and modern e-commerce-style UI

**🛠️ Technologies Used**

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite
- Git & GitHub

##**📂 Project Structure**

CodeAlpha_Ecommerce/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── store/
│   ├── init.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── routing.py
│   ├── consumers.py
│   ├── realtime.py
│   ├── migrations/
│   └── management/
│
├── templates/
│   ├── admin/
│   └── other HTML templates
│
├── static/
│   ├── css/
│   └── js/
│
└── shopease/
├── init.py
├── settings.py
├── urls.py
├── middleware.py
├── asgi.py
└── wsgi.py

##**⚙️ Installation and Setup**

1. Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CodeAlpha_Ecommerce

2. Create a Virtual Environment

python -m venv venv

3. Activate the Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

4. Install Dependencies

pip install -r requirements.txt

5. Apply Database Migrations

python manage.py migrate

6. Start the Development Server

python manage.py runserver

7. Open ShopEase

Open the local server URL shown in the terminal, usually:

http://127.0.0.1:8000/

##**🔐 Security**

Sensitive files and local development files such as the following should be excluded from the repository:

.env
venv/
.venv/
pycache/

API keys, passwords, and other private credentials should never be committed to GitHub.

##**🎯 Internship Project**

Internship: CodeAlpha Full Stack Development Internship

Project: E-Commerce Website

Application Name: ShopEase

Tagline: An e-commerce platform where you explore products, shop online, and connect with products through ratings and reviews.

ShopEase was developed to demonstrate full-stack web development concepts including product management, shopping cart functionality, order management, customer reviews and ratings, responsive UI design, admin management, and dynamic web functionality.

##**👩‍💻 Developed By**

**Ranjani Pullati**

⭐ If you find this project interesting, feel free to explore the repository and its features.
