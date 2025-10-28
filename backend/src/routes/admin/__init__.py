from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ...models import db, User, Category, Product

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not all([email, password]):
        return jsonify({"message": "Email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401
    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
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
    user = User.query.get(int(current_user_id))
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    image = data.get("image")
    if not name:
        return jsonify({"message": "Name is required"}), 400
    category = Category(name=name, description=description, image=image)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Category created", "id": category.id}), 201


@admin_bp.route("/categories/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
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


@admin_bp.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    for key in ["name", "description", "image"]:
        if key in data:
            setattr(category, key, data[key])
    db.session.commit()
    return jsonify({"message": "Category updated"}), 200


@admin_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
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
    user = User.query.get(int(current_user_id))
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
    user = User.query.get(int(current_user_id))
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


@admin_bp.route("/categories", methods=["GET"])
@jwt_required()
def get_categories():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    categories = Category.query.all()
    category_list = [
        {"id": c.id, "name": c.name, "description": c.description, "image": c.image}
        for c in categories
    ]
    return jsonify({"categories": category_list}), 200


@admin_bp.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", type=str)

    query = Product.query

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
            "category": {"name": p.category.name} if p.category else None,
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
