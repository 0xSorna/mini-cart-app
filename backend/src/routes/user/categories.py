from flask import Blueprint, jsonify
from ...models import Category

category_bp = Blueprint("category", __name__)


@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    category_list = [
        {"id": c.id, "name": c.name, "description": c.description} for c in categories
    ]
    return jsonify({"categories": category_list}), 200


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return (
        jsonify(
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            }
        ),
        200,
    )
