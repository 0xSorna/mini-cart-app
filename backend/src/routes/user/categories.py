from flask import Blueprint, jsonify
from ...models import Category

category_bp = Blueprint("category", __name__)


@category_bp.route("/", methods=["GET"])
def get_categories():
    """
    Get all categories.

    Returns:
    - categories: List of category objects with id, name, description, image
    """
    try:
        categories = Category.query.all()
        category_list = [
            {"id": c.id, "name": c.name, "description": c.description, "image": c.image}
            for c in categories
        ]
        return jsonify({"categories": category_list}), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch categories", "error": str(e)}), 500


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """
    Get a single category by ID.

    Parameters:
    - category_id (int): Category ID

    Returns:
    - Category object with id, name, description, image
    """
    try:
        category = Category.query.get_or_404(category_id)
        return (
            jsonify(
                {
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "image": category.image,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": "Category not found", "error": str(e)}), 404
