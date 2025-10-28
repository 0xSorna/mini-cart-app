from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models import db, User, Category, Product

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    users = User.query.all()
    user_list = [
        {"id": u.id, "name": u.name, "email": u.email, "is_admin": u.is_admin}
        for u in users
    ]
    return jsonify({"users": user_list}), 200


@admin_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    if not name:
        return jsonify({"message": "Name is required"}), 400
    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Category created", "id": category.id}), 201


@admin_bp.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    category.name = data.get("name", category.name)
    category.description = data.get("description", category.description)
    db.session.commit()
    return jsonify({"message": "Category updated"}), 200


@admin_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


@admin_bp.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    data = request.get_json()
    if not all(k in data for k in ("name", "title", "price", "category_id")):
        return (
            jsonify({"message": "Required fields: name, title, price, category_id"}),
            400,
        )
    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"message": "Invalid category"}), 400
    product = Product(
        name=data["name"],
        title=data["title"],
        price=data["price"],
        category_id=data["category_id"],
        description=data.get("description"),
        image=data.get("image"),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created", "id": product.id}), 201


@admin_bp.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            return jsonify({"message": "Invalid category"}), 400
    for key in ["name", "title", "price", "category_id", "description", "image"]:
        if key in data:
            setattr(product, key, data[key])
    db.session.commit()
    return jsonify({"message": "Product updated"}), 200


@admin_bp.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
