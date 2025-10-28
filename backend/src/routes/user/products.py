from flask import Blueprint, request, jsonify
from ...models import Product

product_bp = Blueprint("product", __name__)


@product_bp.route("/", methods=["GET"])
def get_products():
    """
    Get paginated list of products with optional filtering.

    Query Parameters:
    - page (int): Page number (default: 1)
    - per_page (int): Products per page (default: 10)
    - category_id (int): Filter by category
    - search (str): Search in product name or title (case-insensitive)
    """
    try:
        # Parse query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        category_id = request.args.get("category_id", type=int)
        search = request.args.get("search", type=str)

        # Build query
        query = Product.query

        # Apply filters
        if category_id:
            query = query.filter_by(category_id=category_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Product.name.ilike(search_term)) | (Product.title.ilike(search_term))
            )

        # Execute paginated query
        products = query.paginate(page=page, per_page=per_page, error_out=False)

        # Format response
        product_list = [
            {
                "id": p.id,
                "name": p.name,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "image": p.image,
                "category_id": p.category_id,
                "rating": p.rating,
                "stock_quantity": (p.id * 7) % 20 + 5,  # Hardcoded stock: 5-24 items
            }
            for p in products.items
        ]

        return (
            jsonify(
                {
                    "products": product_list,
                    "total": products.total,
                    "pages": products.pages,
                    "current_page": page,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"message": "Failed to fetch products", "error": str(e)}), 500


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Get a single product by ID.

    Parameters:
    - product_id (int): Product ID
    """
    try:
        product = Product.query.get_or_404(product_id)

        # Generate a pseudo-random rating based on product ID for consistency
        # But make it more realistic with some variation
        base_rating = (product_id * 0.37) % 3  # 0-3 range
        rating = round(3.5 + base_rating, 1)  # 3.5 to 4.5 range
        if rating > 5.0:
            rating = 5.0

        return (
            jsonify(
                {
                    "id": product.id,
                    "name": product.name,
                    "title": product.title,
                    "description": product.description,
                    "price": product.price,
                    "image": product.image,
                    "category_id": product.category_id,
                    "category_name": (
                        product.category.name if product.category else None
                    ),
                    "rating": rating,
                    "stock_quantity": (product_id * 7) % 20
                    + 5,  # Hardcoded stock: 5-24 items per product
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": "Product not found", "error": str(e)}), 404
