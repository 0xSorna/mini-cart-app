from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models import db, ShoppingCart, CartItem, Product


cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/", methods=["GET", "OPTIONS"])
@jwt_required()
def get_cart():
    current_user_id = int(get_jwt_identity())
    cart = ShoppingCart.query.filter_by(
        user_id=current_user_id, status="active"
    ).first()
    if not cart:
        return jsonify({"cart_items": []}), 200
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    item_list = [
        {
            "id": ci.id,
            "product_id": ci.product_id,
            "quantity": ci.quantity,
            "price_at_time": ci.price_at_time,
            "product": {
                "name": ci.product.name,
                "price": ci.product.price,
                "image_url": ci.product.image,
            },
        }
        for ci in cart_items
    ]
    return jsonify({"cart_items": item_list}), 200


@cart_bp.route("/add", methods=["POST", "OPTIONS"])
@jwt_required()
def add_to_cart():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    if not product_id:
        return jsonify({"message": "Product ID required"}), 400
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    cart = ShoppingCart.query.filter_by(
        user_id=current_user_id, status="active"
    ).first()
    if not cart:
        cart = ShoppingCart(user_id=current_user_id)
        db.session.add(cart)
        db.session.commit()
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price_at_time=product.price,
        )
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Added to cart"}), 200


@cart_bp.route("/update/<int:item_id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_cart_item(item_id):
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    quantity = data.get("quantity")
    if quantity is None or quantity <= 0:
        return jsonify({"message": "Valid quantity required"}), 400
    cart_item = CartItem.query.get_or_404(item_id)
    cart = cart_item.cart
    if cart.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({"message": "Cart item updated"}), 200


@cart_bp.route("/remove/<int:item_id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
def remove_cart_item(item_id):
    current_user_id = int(get_jwt_identity())
    cart_item = CartItem.query.get_or_404(item_id)
    cart = cart_item.cart
    if cart.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Removed from cart"}), 200
