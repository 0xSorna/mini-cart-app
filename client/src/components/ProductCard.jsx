import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../utils/api';

const ProductCard = ({ product }) => {
  const navigate = useNavigate();
  const [addingToCart, setAddingToCart] = useState(false);
  const imageUrl = product.image || 'https://via.placeholder.com/300x200?text=No+Image';

  const handleAddToCart = async (e) => {
    e.preventDefault();
    e.stopPropagation();

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        navigate('/login');
        return;
      }

      setAddingToCart(true);
      const cartData = {
        product_id: product.id,
        quantity: 1
      };

      await api.post('/cart/add', cartData);
      alert(`Added ${product.name} to cart!`);
    } catch (error) {
      console.error('Error adding to cart:', error);
      alert('Error adding product to cart');
    } finally {
      setAddingToCart(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <Link to={`/products/${product.id}`}>
        <img
          src={imageUrl}
          alt={product.name}
          className="w-full h-48 object-cover hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x200?text=No+Image';
          }}
        />
      </Link>

      <div className="p-4">
        <Link to={`/products/${product.id}`}>
          <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600">
            {product.name}
          </h3>
        </Link>

        <p className="text-gray-600 text-sm mb-2 line-clamp-2">
          {product.description}
        </p>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-2xl font-bold text-green-600">
              ₹{product.price}
            </span>
            {product.discount_price && product.discount_price < product.price && (
              <span className="text-sm text-gray-500 line-through ml-2">
                ₹{product.discount_price}
              </span>
            )}
          </div>

          <button
            onClick={handleAddToCart}
            disabled={addingToCart}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {addingToCart ? 'Adding...' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
