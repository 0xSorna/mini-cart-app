from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models import db, Category, User

admin_bp = Blueprint("admin_categories", __name__)


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
