import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../utils/api';

const Cart = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchCartItems();
  }, []);

  const fetchCartItems = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await api.get('/cart');
      setCartItems(response.data.cart_items || []);
    } catch (error) {
      console.error('Error fetching cart items:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (cartId, newQuantity) => {
    if (newQuantity < 1) return;

    setUpdating(true);
    try {
      await api.put(`/cart/update/${cartId}`, { quantity: newQuantity });
      await fetchCartItems();
    } catch (error) {
      console.error('Error updating quantity:', error);
      alert('Error updating quantity');
    } finally {
      setUpdating(false);
    }
  };

  const removeItem = async (cartId) => {
    setUpdating(true);
    try {
      await api.delete(`/cart/remove/${cartId}`);
      await fetchCartItems();
    } catch (error) {
      console.error('Error removing item:', error);
      alert('Error removing item');
    } finally {
      setUpdating(false);
    }
  };

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  };

  const getTotalItems = () => {
    return cartItems.reduce((total, item) => total + item.quantity, 0);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading your cart...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Shopping Cart</h1>
          <span className="text-gray-600">({getTotalItems()} items)</span>
        </div>

        {cartItems.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <svg className="mx-auto h-24 w-24 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1 4H20M7 13v4a2 2 0 002 2h10a2 2 0 002-2v-4" />
            </svg>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Your cart is empty</h2>
            <p className="text-gray-600 mb-6">Looks like you haven't added any products to your cart yet.</p>
            <Link
              to="/products"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Shopping
            </Link>
          </div>
        ) : (
          <>
             <div className="bg-white rounded-lg shadow-md">
              {cartItems.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center p-6 border-b border-gray-200 last:border-b-0"
                >
               
                  <img
                    src={item.product.image_url || 'https://via.placeholder.com/100x100?text=No+Image'}
                    alt={item.product.name}
                    className="w-20 h-20 object-cover rounded-lg mr-4"
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/100x100?text=No+Image';
                    }}
                  />

             
                  <div className="flex-1">
                    <Link
                      to={`/products/${item.product.id}`}
                      className="text-lg font-semibold text-gray-900 hover:text-blue-600"
                    >
                      {item.product.name}
                    </Link>
                    <p className="text-gray-600 text-sm mt-1">
                      ₹{item.product.price} each
                    </p>
                  </div>

                
                  <div className="flex items-center space-x-2 mx-4">
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      disabled={updating}
                      className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center disabled:opacity-50"
                    >
                      -
                    </button>
                    <span className="w-12 text-center">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      disabled={updating}
                      className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center disabled:opacity-50"
                    >
                      +
                    </button>
                  </div>

                 
                  <span className="text-lg font-semibold text-gray-900 mx-4">
                    ₹{(item.product.price * item.quantity).toFixed(2)}
                  </span>

                 
                  <button
                    onClick={() => removeItem(item.id)}
                    disabled={updating}
                    className="text-red-600 hover:text-red-800 disabled:opacity-50"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.14A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.86L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Summary</h2>

              <div className="space-y-3 mb-6">
                <div className="flex justify-between">
                  <span className="text-gray-600">Items ({getTotalItems()})</span>
                  <span className="font-semibold text-gray-900">
                    ₹{getTotalPrice().toFixed(2)}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-600">Shipping</span>
                  <span className="font-semibold text-gray-900">
                    {getTotalPrice() > 50 ? 'Free' : '₹5.99'}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-600">Tax</span>
                  <span className="font-semibold text-gray-900">
                    ₹{(getTotalPrice() * 0.08).toFixed(2)}
                  </span>
                </div>
              </div>

              <hr className="my-6" />

              <div className="flex justify-between items-center mb-6">
                <span className="text-2xl font-bold">Total</span>
                <span className="text-2xl font-bold text-green-600">
                  ₹{(getTotalPrice() + (getTotalPrice() > 50 ? 0 : 5.99) + (getTotalPrice() * 0.08)).toFixed(2)}
                </span>
              </div>

              <button
                onClick={() => navigate('/checkout')}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
              >
                Proceed to Checkout
              </button>

              <Link
                to="/products"
                className="w-full block text-center mt-4 text-blue-600 hover:text-blue-800"
              >
                Continue Shopping
              </Link>
            </div>

          
           
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;
