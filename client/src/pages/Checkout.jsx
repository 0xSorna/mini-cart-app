import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';

const Checkout = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    shipping_address: '',
    billing_address: '',
  });

  const [useSameAddress, setUseSameAddress] = useState(true);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    fetchCartItems();

    if (useSameAddress && formData.shipping_address) {
      setFormData(prev => ({
        ...prev,
        billing_address: prev.shipping_address
      }));
    }
  }, [useSameAddress]);

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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }

    // Update billing address if using same address
    if (name === 'shipping_address' && useSameAddress) {
      setFormData(prev => ({
        ...prev,
        billing_address: value
      }));
    }
  };

  const handleUseSameAddressChange = (e) => {
    setUseSameAddress(e.target.checked);
    if (e.target.checked) {
      setFormData(prev => ({
        ...prev,
        billing_address: prev.shipping_address
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.shipping_address.trim()) {
      newErrors.shipping_address = 'Shipping address is required';
    }

    if (!formData.billing_address.trim()) {
      newErrors.billing_address = 'Billing address is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setSubmitting(true);

    try {
      const orderData = {
        shipping_address: formData.shipping_address,
        billing_address: formData.billing_address,
      };

      await api.post('/orders/place', orderData);

      // Clear cart and redirect to success page
      alert('Order placed successfully! Cash on Delivery.');
      navigate('/');
    } catch (error) {
      console.error('Error placing order:', error);
      alert('Error placing order. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  };

  const getShippingCost = () => {
    return getTotalPrice() > 50 ? 0 : 5.99;
  };

  const getTax = () => {
    return getTotalPrice() * 0.08;
  };

  const getTotal = () => {
    return getTotalPrice() + getShippingCost() + getTax();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading checkout...</p>
          </div>
        </div>
      </div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-900">No items to checkout</h2>
            <p className="text-gray-600 mt-2">Please add items to your cart first.</p>
            <button
              onClick={() => navigate('/products')}
              className="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Start Shopping
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Checkout</h1>
        </div>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Checkout Form */}
          <div className="lg:col-span-2">
            {/* Shipping Address */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-xl font-semibold mb-4">Shipping Address</h2>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Shipping Address
                </label>
                <textarea
                  name="shipping_address"
                  value={formData.shipping_address}
                  onChange={handleInputChange}
                  rows={4}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.shipping_address ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="Enter your full shipping address including street, city, state, pincode"
                />
                {errors.shipping_address && (
                  <p className="text-red-500 text-sm mt-1">{errors.shipping_address}</p>
                )}
              </div>
            </div>

            {/* Billing Address */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <div className="flex items-center mb-4">
                <input
                  type="checkbox"
                  id="same_address"
                  checked={useSameAddress}
                  onChange={handleUseSameAddressChange}
                  className="mr-2"
                />
                <label htmlFor="same_address" className="text-sm font-medium text-gray-700">
                  Billing address same as shipping address
                </label>
              </div>

              {!useSameAddress && (
                <>
                  <h2 className="text-xl font-semibold mb-4">Billing Address</h2>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Billing Address
                    </label>
                    <textarea
                      name="billing_address"
                      value={formData.billing_address}
                      onChange={handleInputChange}
                      rows={4}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.billing_address ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Enter your full billing address including street, city, state, pincode"
                    />
                    {errors.billing_address && (
                      <p className="text-red-500 text-sm mt-1">{errors.billing_address}</p>
                    )}
                  </div>
                </>
              )}
            </div>

            {/* Payment Information - Cash on Delivery */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Payment Method</h2>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span className="text-green-800 font-medium">Cash on Delivery (COD)</span>
                </div>
                <p className="text-green-700 text-sm mt-1">
                  Pay in cash when your order is delivered to your doorstep. No advance payment required.
                </p>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
              <h2 className="text-xl font-semibold mb-4">Order Summary</h2>

              {/* Order Items */}
              <div className="space-y-3 mb-6">
                {cartItems.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {item.product.name} x{item.quantity}
                    </span>
                    <span className="font-semibold">
                      ₹{(item.product.price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>

              <hr className="my-4" />

              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span>₹{getTotalPrice().toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Shipping</span>
                  <span>{getShippingCost() === 0 ? 'Free' : `₹${getShippingCost().toFixed(2)}`}</span>
                </div>
                <div className="flex justify-between">
                  <span>Tax</span>
                  <span>₹{getTax().toFixed(2)}</span>
                </div>
              </div>

              <hr className="my-4" />

              <div className="flex justify-between text-xl font-bold mb-6">
                <span>Total</span>
                <span className="text-green-600">₹{getTotal().toFixed(2)}</span>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-semibold disabled:opacity-50"
              >
                {submitting ? 'Placing Order...' : 'Place Order (Cash on Delivery)'}
              </button>

              <div className="mt-4 text-center">
                <button
                  type="button"
                  onClick={() => navigate('/cart')}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  ← Back to Cart
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Checkout;
