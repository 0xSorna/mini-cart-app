from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ...models import db, User, Category, Product, Order

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard_stats():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    from sqlalchemy import func, extract

    # Count stats
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()

    # Active orders count
    active_orders = Order.query.filter(
        Order.status.in_(["pending", "confirmed", "shipped"])
    ).count()

    # Revenue stats
    total_revenue = (
        db.session.query(func.sum(Order.total_amount))
        .filter(Order.status.in_(["confirmed", "shipped", "delivered"]))
        .scalar()
        or 0
    )
    monthly_revenue = (
        db.session.query(func.sum(Order.total_amount))
        .filter(
            Order.status.in_(["confirmed", "shipped", "delivered"]),
            extract("month", Order.created_at)
            == db.func.extract("month", db.func.now()),
        )
        .scalar()
        or 0
    )

    # Recent orders (last 5)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_orders_data = [
        {
            "id": o.id,
            "user_name": o.user.name,
            "total_amount": o.total_amount,
            "status": o.status,
            "created_at": o.created_at.isoformat(),
        }
        for o in recent_orders
    ]

    # Category distribution
    product_categories = (
        db.session.query(Category.name, func.count(Product.id).label("count"))
        .join(Product)
        .group_by(Category.id)
        .all()
    )

    category_data = [{"name": cat[0], "count": cat[1]} for cat in product_categories]

    # Monthly order trend (last 6 months)
    from datetime import datetime, timedelta

    monthly_orders = {}
    for i in range(5, -1, -1):  # Last 6 months
        month_start = datetime.now() - timedelta(days=30 * i)
        month_end = month_start + timedelta(days=30)
        count = Order.query.filter(
            Order.created_at >= month_start, Order.created_at < month_end
        ).count()
        monthly_orders[month_start.strftime("%B")] = count

    return (
        jsonify(
            {
                "stats": {
                    "total_products": total_products,
                    "total_categories": total_categories,
                    "total_users": total_users,
                    "total_orders": total_orders,
                    "active_orders": active_orders,
                    "total_revenue": total_revenue,
                    "monthly_revenue": monthly_revenue,
                },
                "recent_orders": recent_orders_data,
                "categories": category_data,
                "monthly_orders": monthly_orders,
            }
        ),
        200,
    )


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


@admin_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_all_orders():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    from sqlalchemy import desc
    from ...models import Order

    orders = Order.query.order_by(desc(Order.created_at)).all()
    order_list = [
        {
            "id": o.id,
            "user_id": o.user_id,
            "user_name": o.user.name,
            "user_email": o.user.email,
            "total_amount": o.total_amount,
            "status": o.status,
            "created_at": o.created_at.isoformat(),
            "shipping_address": o.shipping_address,
            "billing_address": o.billing_address,
        }
        for o in orders
    ]
    return jsonify({"orders": order_list}), 200


@admin_bp.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order_detail(order_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    from ...models import Order

    order = Order.query.get_or_404(order_id)

    items = [
        {
            "id": oi.id,
            "product_id": oi.product_id,
            "quantity": oi.quantity,
            "price": oi.price,
            "product": {"name": oi.product.name, "image": oi.product.image},
        }
        for oi in order.items
    ]

    return (
        jsonify(
            {
                "id": order.id,
                "user_id": order.user_id,
                "user_name": order.user.name,
                "user_email": order.user.email,
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "shipping_address": order.shipping_address,
                "billing_address": order.billing_address,
                "items": items,
            }
        ),
        200,
    )


@admin_bp.route("/orders/<int:order_id>/status", methods=["PUT"])
@jwt_required()
def update_order_status(order_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    from ...models import Order

    data = request.get_json()
    new_status = data.get("status")

    valid_statuses = ["pending", "confirmed", "shipped", "delivered"]
    if new_status not in valid_statuses:
        return jsonify({"message": "Invalid status"}), 400

    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Order status updated",
                "order_id": order.id,
                "status": order.status,
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
