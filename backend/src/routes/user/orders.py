from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from ...models import db, ShoppingCart, Order, OrderItem

order_bp = Blueprint("order", __name__)


# ORDER MANAGEMENT ENDPOINTS (Cash on Delivery Only)


@order_bp.route("/place", methods=["POST"])
@jwt_required()
def place_order():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    shipping_address = data.get("shipping_address")
    billing_address = data.get("billing_address", shipping_address)
    if not shipping_address:
        return jsonify({"message": "Shipping address required"}), 400
    cart = ShoppingCart.query.filter_by(
        user_id=current_user_id, status="active"
    ).first()
    if not cart or not cart.items:
        return jsonify({"message": "Cart is empty"}), 400
    total = sum(ci.quantity * ci.price_at_time for ci in cart.items)
    order = Order(
        user_id=current_user_id,
        total_amount=total,
        shipping_address=shipping_address,
        billing_address=billing_address,
    )
    db.session.add(order)
    db.session.commit()
    for ci in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=ci.product_id,
            quantity=ci.quantity,
            price=ci.price_at_time,
        )
        db.session.add(order_item)
    cart.status = "checked_out"
    db.session.commit()
    return jsonify({"message": "Order placed", "order_id": order.id}), 201


@order_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():
    current_user_id = int(get_jwt_identity())
    orders = (
        Order.query.filter_by(user_id=current_user_id)
        .order_by(desc(Order.created_at))
        .all()
    )
    order_list = [
        {
            "id": o.id,
            "total_amount": o.total_amount,
            "status": o.status,
            "created_at": o.created_at.isoformat(),
            "shipping_address": o.shipping_address,
            "billing_address": o.billing_address,
        }
        for o in orders
    ]
    return jsonify({"orders": order_list}), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    current_user_id = int(get_jwt_identity())
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
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
