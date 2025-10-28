from flask import Blueprint, request, jsonify
from ...models import Product

product_bp = Blueprint("product", __name__)


@product_bp.route("/", methods=["GET"])
def get_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category_id = request.args.get("category_id", type=int)
    search = request.args.get("search", type=str)

    query = Product.query

    if category_id:
        query = query.filter_by(category_id=category_id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) | (Product.title.ilike(search_term))
        )

    products = query.paginate(page=page, per_page=per_page, error_out=False)
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


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
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
                "rating": product.rating,
            }
        ),
        200,
    )
