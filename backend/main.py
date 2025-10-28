import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models import User, db
from src.routes import (
    auth_bp,
    admin_bp,
    category_bp,
    product_bp,
    cart_bp,
    order_bp,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.abspath('instance/ecom.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5000",
        "https://mini-cart-app.vercel.app",
        "https://mini-cart-app.onrender.com",
    ],
    methods=["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "X-Login-Request"],
)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        origin = request.headers.get("Origin", "")
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5000",
            "https://mini-cart-app.vercel.app",
            "https://mini-cart-app.onrender.com",
        ]
        if origin in allowed_origins:
            response.headers.add("Access-Control-Allow-Origin", origin)
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,X-Login-Request"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,HEAD,POST,PUT,DELETE,OPTIONS"
        )
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200


jwt = JWTManager(app)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return (
        jsonify({"error": "Unauthorized", "message": "Missing or invalid token"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_response(callback):
    return (
        jsonify({"error": "Invalid token", "message": "The JWT token is invalid"}),
        401,
    )


db.init_app(app)

with app.app_context():
    db.create_all()
    admin = db.session.execute(
        db.select(User).filter_by(email="admin@example.com")
    ).scalar_one_or_none()
    if not admin:
        admin = User(name="Admin", email="admin@example.com", is_admin=True)
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.commit()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(category_bp, url_prefix="/categories")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(order_bp, url_prefix="/orders")


@app.route("/")
def hello():
    return "Ecommerce Backend Running!"


if __name__ == "__main__":
    app.run(debug=True)
