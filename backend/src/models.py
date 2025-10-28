from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(500))  # Image URL or path

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))  # Image URL or path
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    rating = db.Column(db.Float, default=0.0)

    category = db.relationship("Category", backref=db.backref("products", lazy=True))

    def __repr__(self):
        return f"<Product {self.name}>"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1-5
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    product = db.relationship("Product", backref=db.backref("reviews", lazy=True))
    user = db.relationship("User", backref=db.backref("reviews", lazy=True))

    def __repr__(self):
        return f"<Review {self.id} for product {self.product_id}>"


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default="active")  # active, checked_out

    user = db.relationship("User", backref=db.backref("carts", lazy=True))

    def __repr__(self):
        return f"<ShoppingCart {self.id} for user {self.user_id}>"


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("shopping_cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_time = db.Column(db.Float, nullable=False)  # To keep price if it changes

    cart = db.relationship("ShoppingCart", backref=db.backref("items", lazy=True))
    product = db.relationship("Product", backref=db.backref("cart_items", lazy=True))

    def __repr__(self):
        return f"<CartItem {self.quantity} x {self.product_id}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.String(50), default="pending"
    )  # pending, confirmed, shipped, delivered
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    shipping_address = db.Column(db.Text)
    billing_address = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("orders", lazy=True))

    def __repr__(self):
        return f"<Order {self.id} for user {self.user_id}>"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", backref=db.backref("items", lazy=True))
    product = db.relationship("Product", backref=db.backref("order_items", lazy=True))

    def __repr__(self):
        return f"<OrderItem {self.quantity} x {self.product_id}>"
