from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.contrib.auth.models import User
from django.db import transaction, models
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from .models import (
    Category,
    Product,
    CartItem,
    Order,
    OrderItem,
    Review
)

from .realtime import (
    broadcast_order,
    broadcast_review
)


# =========================================================
# CART DATA
# =========================================================

def cart_data(request):

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related(
            "product",
            "product__category"
        )
    )

    items = []
    total = Decimal("0")
    count = 0

    for item in cart_items:

        product = item.product

        # Remove products which are out of stock
        if product.stock <= 0:
            item.delete()
            continue

        # Make sure cart quantity never exceeds stock
        if item.quantity > product.stock:

            item.quantity = product.stock

            item.save(
                update_fields=[
                    "quantity",
                    "updated_at"
                ]
            )

        line_total = (
            product.price * item.quantity
        )

        items.append({
            "product": product,
            "quantity": item.quantity,
            "line_total": line_total,
        })

        total += line_total
        count += item.quantity

    return items, total, count


# =========================================================
# HOME + SMART SEARCH
# =========================================================

def home(request):

    products = (
        Product.objects
        .select_related("category")
        .all()
        .order_by("-created_at")
    )

    query = (
        request.GET
        .get("q", "")
        .strip()
    )

    category = (
        request.GET
        .get("category", "")
        .strip()
    )

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    if category:

        products = products.filter(
            category__slug=category
        )

    # -----------------------------------------------------
    # SMART SEARCH
    # -----------------------------------------------------

    if query:

        search_text = query.lower().strip()

        # Words that don't affect product search
        ignored_words = {
            "for",
            "the",
            "a",
            "an",
            "and",
            "of",
            "in",
            "with",
            "on",
            "to",
        }

        words = [
            word
            for word in search_text.split()
            if word not in ignored_words
        ]

        # -------------------------------------------------
        # GENDER KEYWORDS
        # -------------------------------------------------

        gender_map = {

            "boy": "Boys",
            "boys": "Boys",

            "girl": "Girls",
            "girls": "Girls",

            "man": "Men",
            "men": "Men",

            "woman": "Women",
            "women": "Women",

            "unisex": "Unisex",
        }

        # -------------------------------------------------
        # PRODUCT TYPE KEYWORDS
        # -------------------------------------------------

        type_map = {

            "jean": "Jeans",
            "jeans": "Jeans",

            "shirt": "Shirt",
            "shirts": "Shirt",

            "top": "Top",
            "tops": "Top",

            "tshirt": "T-Shirt",
            "tshirts": "T-Shirt",
            "tee": "T-Shirt",
            "tees": "T-Shirt",

            "t-shirt": "T-Shirt",
            "t-shirts": "T-Shirt",

            "jacket": "Jacket",
            "jackets": "Jacket",

            "pant": "Pants",
            "pants": "Pants",

            "hoodie": "Hoodie",
            "hoodies": "Hoodie",

            "sweatshirt": "Sweatshirt",
            "sweatshirts": "Sweatshirt",

            "shoe": "Shoes",
            "shoes": "Shoes",

            "accessory": "Accessories",
            "accessories": "Accessories",
        }

        # -------------------------------------------------
        # GENERAL CLOTHING SEARCH
        # -------------------------------------------------

        clothing_words = {
            "dress",
            "dresses",
            "clothes",
            "clothing",
            "wear",
            "outfit",
            "outfits",
        }

        detected_gender = None
        detected_type = None
        general_clothing = False

        normal_words = []

        # -------------------------------------------------
        # IDENTIFY SEARCH WORDS
        # -------------------------------------------------

        for word in words:

            clean_word = (
                word
                .replace(",", "")
                .replace(".", "")
                .replace("!", "")
                .replace("?", "")
                .strip()
            )

            if not clean_word:
                continue

            # Gender
            if clean_word in gender_map:

                detected_gender = gender_map[
                    clean_word
                ]

            # General clothing
            elif clean_word in clothing_words:

                general_clothing = True

            # Specific product type
            elif clean_word in type_map:

                detected_type = type_map[
                    clean_word
                ]

            # Normal search word
            else:

                normal_words.append(
                    clean_word
                )

        # -------------------------------------------------
        # APPLY GENDER
        # -------------------------------------------------

        if detected_gender:

            products = products.filter(
                gender=detected_gender
            )

        # -------------------------------------------------
        # APPLY PRODUCT TYPE
        # -------------------------------------------------

        if detected_type:

            products = products.filter(
                product_type=detected_type
            )

        # -------------------------------------------------
        # GENERAL CLOTHING SEARCH
        # -------------------------------------------------
        #
        # Example:
        #
        # boys dresses
        #
        # means all clothing products for Boys.
        #
        # It should NOT mean only Product Type = Dress.
        # -------------------------------------------------

        elif general_clothing:

            clothing_types = [
                "Jeans",
                "Shirt",
                "T-Shirt",
                "Dress",
                "Jacket",
                "Pants",
                "Hoodie",
                "Sweatshirt",
                "Shoes",
                "Accessories",
                "Other",
            ]

            products = products.filter(
                product_type__in=clothing_types
            )

        # -------------------------------------------------
        # SEARCH REMAINING WORDS
        # -------------------------------------------------

        for word in normal_words:

            products = products.filter(
                models.Q(
                    name__icontains=word
                )
                |
                models.Q(
                    description__icontains=word
                )
                |
                models.Q(
                    category__name__icontains=word
                )
            )

    # -----------------------------------------------------
    # FEATURED PRODUCTS
    # -----------------------------------------------------

    featured = (
        Product.objects
        .filter(featured=True)
        .order_by("-created_at")[:4]
    )

    # -----------------------------------------------------
    # HOME PAGE
    # -----------------------------------------------------

    return render(
        request,
        "home.html",
        {
            "products": products,

            "categories": (
                Category.objects
                .all()
                .order_by("name")
            ),

            "featured": featured,

            "query": query,
        }
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail(request, pk):

    product = get_object_or_404(
        Product.objects.select_related(
            "category"
        ),
        pk=pk
    )

    reviews = (
        product.reviews
        .select_related("user")
        .all()
    )

    related = (
        Product.objects
        .filter(
            category=product.category
        )
        .exclude(pk=pk)
        .select_related("category")[:4]
    )

    user_review = None

    if request.user.is_authenticated:

        user_review = (
            reviews
            .filter(
                user=request.user
            )
            .first()
        )

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "related": related,
            "reviews": reviews,
            "user_review": user_review,
        }
    )


# =========================================================
# ADD / UPDATE REVIEW
# =========================================================

@login_required
def add_review(request, pk):

    if request.method != "POST":

        return redirect(
            "product_detail",
            pk=pk
        )

    product = get_object_or_404(
        Product,
        pk=pk
    )

    try:

        rating = int(
            request.POST.get(
                "rating",
                "0"
            )
        )

    except (
        TypeError,
        ValueError
    ):

        rating = 0

    comment = (
        request.POST
        .get("comment", "")
        .strip()
    )

    if rating not in range(1, 6):

        messages.error(
            request,
            "Please select a rating from 1 to 5 stars."
        )

        return redirect(
            "product_detail",
            pk=pk
        )

    # Only customers who purchased the product
    # can submit a review.

    has_purchased = (
        OrderItem.objects
        .filter(
            order__user=request.user,
            product=product
        )
        .exists()
    )

    if not has_purchased:

        messages.error(
            request,
            "You can review this product after purchasing it."
        )

        return redirect(
            "product_detail",
            pk=pk
        )

    review, created = (
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                "rating": rating,
                "comment": comment,
            }
        )
    )

    transaction.on_commit(
        lambda: broadcast_review(review)
    )

    if created:

        messages.success(
            request,
            "Your review has been added."
        )

    else:

        messages.success(
            request,
            "Your review has been updated."
        )

    return redirect(
        "product_detail",
        pk=pk
    )


# =========================================================
# ADD TO CART
# =========================================================

@login_required
def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if product.stock <= 0:

        messages.error(
            request,
            "This product is currently out of stock."
        )

        return redirect(
            "product_detail",
            pk=pk
        )

    cart_item, created = (
        CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                "quantity": 1
            }
        )
    )

    if not created:

        if cart_item.quantity >= product.stock:

            messages.warning(
                request,
                "You already have the maximum available stock in your cart."
            )

        else:

            cart_item.quantity += 1

            cart_item.save(
                update_fields=[
                    "quantity",
                    "updated_at"
                ]
            )

            messages.success(
                request,
                f"{product.name} added to your cart."
            )

    else:

        messages.success(
            request,
            f"{product.name} added to your cart."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER"
        ) or "home"
    )


# =========================================================
# CART PAGE
# =========================================================

@login_required
def cart(request):

    items, total, count = cart_data(
        request
    )

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total,
            "count": count,
        }
    )


# =========================================================
# UPDATE CART
# =========================================================

@login_required
def update_cart(request, pk):

    if request.method != "POST":

        return redirect("cart")

    product = get_object_or_404(
        Product,
        pk=pk
    )

    try:

        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )

    except (
        TypeError,
        ValueError
    ):

        quantity = 1

    cart_item = (
        CartItem.objects
        .filter(
            user=request.user,
            product=product
        )
        .first()
    )

    if not cart_item:

        messages.error(
            request,
            "This product is not in your cart."
        )

        return redirect("cart")

    if product.stock <= 0:

        cart_item.delete()

        messages.warning(
            request,
            "This product is out of stock."
        )

        return redirect("cart")

    quantity = max(
        1,
        min(
            quantity,
            product.stock
        )
    )

    cart_item.quantity = quantity

    cart_item.save(
        update_fields=[
            "quantity",
            "updated_at"
        ]
    )

    messages.success(
        request,
        "Cart updated successfully."
    )

    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

@login_required
def remove_from_cart(request, pk):

    CartItem.objects.filter(
        user=request.user,
        product_id=pk
    ).delete()

    messages.success(
        request,
        "Product removed from your cart."
    )

    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================

@login_required
@transaction.atomic
def checkout(request):

    if request.method == "POST":

        required = [
            "full_name",
            "email",
            "address",
            "city",
            "postal_code"
        ]

        # Validate delivery details
        if any(
            not request.POST
            .get(field, "")
            .strip()
            for field in required
        ):

            messages.error(
                request,
                "Please fill in all delivery details."
            )

            items, total, count = cart_data(
                request
            )

            return render(
                request,
                "checkout.html",
                {
                    "items": items,
                    "total": total
                }
            )

        # Get current user's cart only
        cart_items = list(
            CartItem.objects
            .filter(
                user=request.user
            )
            .select_related("product")
        )

        if not cart_items:

            messages.warning(
                request,
                "Your cart is empty."
            )

            return redirect("home")

        fresh_items = []

        final_total = Decimal("0.00")

        # Lock products while checking stock
        for cart_item in cart_items:

            product = (
                Product.objects
                .select_for_update()
                .filter(
                    pk=cart_item.product.pk
                )
                .first()
            )

            if not product:

                messages.error(
                    request,
                    "One of the products is no longer available."
                )

                return redirect("cart")

            quantity = cart_item.quantity

            if (
                quantity < 1
                or product.stock < quantity
            ):

                messages.error(
                    request,
                    f"Only {product.stock} unit(s) of "
                    f"{product.name} are available."
                )

                return redirect("cart")

            fresh_items.append(
                (
                    product,
                    quantity
                )
            )

            final_total += (
                product.price *
                quantity
            )

        if not fresh_items:

            messages.warning(
                request,
                "Your cart is empty."
            )

            return redirect("home")

        # -------------------------------------------------
        # CREATE ORDER
        # -------------------------------------------------

        order = Order.objects.create(

            user=request.user,

            full_name=(
                request.POST["full_name"]
                .strip()
            ),

            email=(
                request.POST["email"]
                .strip()
            ),

            address=(
                request.POST["address"]
                .strip()
            ),

            city=(
                request.POST["city"]
                .strip()
            ),

            postal_code=(
                request.POST["postal_code"]
                .strip()
            ),

            total=final_total
        )

        # -------------------------------------------------
        # CREATE ORDER ITEMS + REDUCE STOCK
        # -------------------------------------------------

        for product, quantity in fresh_items:

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity

            product.save(
                update_fields=[
                    "stock"
                ]
            )

        # Empty current user's cart
        CartItem.objects.filter(
            user=request.user
        ).delete()

        # Notify admin live dashboard
        transaction.on_commit(
            lambda: broadcast_order(
                order,
                "new_order"
            )
        )

        messages.success(
            request,
            f"Order #{order.order_number} placed successfully!"
        )

        return redirect("orders")

    # -----------------------------------------------------
    # GET CHECKOUT PAGE
    # -----------------------------------------------------

    items, total, count = cart_data(
        request
    )

    if not items:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("home")

    return render(
        request,
        "checkout.html",
        {
            "items": items,
            "total": total
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

@login_required
def orders(request):

    user_orders = (
        Order.objects
        .filter(
            user=request.user
        )
        .prefetch_related(
            "items__product"
        )
        .order_by(
            "-created_at"
        )
    )

    return render(
        request,
        "orders.html",
        {
            "orders": user_orders
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        name = (
            request.POST
            .get("username", "")
            .strip()
        )

        email = (
            request.POST
            .get("email", "")
            .strip()
            .lower()
        )

        password = request.POST.get(
            "password",
            ""
        )

        if not name or not email or len(password) < 6:

            messages.error(
                request,
                "Please enter a name, valid email and password of at least 6 characters."
            )

            return render(
                request,
                "register.html"
            )

        # Email must be unique
        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "An account with this email already exists."
            )

            return render(
                request,
                "register.html"
            )

        # Django username must be unique internally.
        # Customer's actual name can still be the same.
        base_username = name.replace(" ", "_")
        username = base_username
        counter = 2

        while User.objects.filter(
            username=username
        ).exists():

            username = f"{base_username}_{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            first_name=name,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect("home")

    return render(
        request,
        "register.html"
    )
# =========================================================
# LOGIN
# =========================================================
def login_view(request):
    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        # Clear any previous logged-in session
        logout(request)

        user = User.objects.filter(email__iexact=email).first()

        if user is not None:
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("home")

        messages.error(request, "Invalid email or password.")

    return render(request, "login.html")

# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")

# =========================================================
# ADMIN SHOP PREVIEW
# =========================================================

@user_passes_test(
    lambda user:
        user.is_authenticated
        and user.is_staff
)
def admin_shop_preview(request):

    products = (
        Product.objects
        .select_related("category")
        .prefetch_related("reviews")
        .order_by("-created_at")
    )

    return render(
        request,
        "admin/shop_preview.html",
        {
            "products": products,
        }
    )

# =========================================================
# ADMIN LIVE ORDERS
# =========================================================

@user_passes_test(
    lambda user:
        user.is_authenticated
        and user.is_staff
)
def live_orders(request):

    recent_orders = (
        Order.objects
        .select_related("user")
        .prefetch_related(
            "items__product"
        )
        .order_by(
            "-created_at"
        )[:20]
    )

    return render(
        request,
        "admin/live_orders.html",
        {
            "recent_orders": recent_orders
        }
    )