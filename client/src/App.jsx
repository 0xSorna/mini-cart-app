import React from 'react';
import { Routes, Route } from 'react-router';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import Register from './pages/Register';
import AuthLayout from './pages/AuthLayout';
import Categories from './pages/Categories';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Category from './pages/Category';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import Orders from './pages/Orders';
import OrderDetail from './pages/OrderDetail';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import AdminProducts from './pages/AdminProducts';
import AdminAddProduct from './pages/AdminAddProduct';
import AdminCategories from './pages/AdminCategories';
import AdminAddCategory from './pages/AdminAddCategory';
import AdminEditCategory from './pages/AdminEditCategory';
import AdminOrders from './pages/AdminOrders';
import AdminUsers from './pages/AdminUsers';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={
          <>
            <Navigation />
            <Home />
          </>
        } />
        <Route path="/about" element={
          <>
            <Navigation />
            <About />
            <Footer />
          </>
        } />
        <Route path="/products" element={
          <>
            <Navigation />
            <Products />
            <Footer />
          </>
        } />
        <Route path="/products/:productId" element={
          <>
            <Navigation />
            <ProductDetail />
            <Footer />
          </>
        } />
        <Route path="/categories" element={
          <>
            <Navigation />
            <Categories />
            <Footer />
          </>
        } />
        <Route path="/categories/:categoryId" element={
          <>
            <Navigation />
            <Category />
            <Footer />
          </>
        } />
        <Route path="/cart" element={
          <>
            <Navigation />
            <Cart />
            <Footer />
          </>
        } />
        <Route path="/checkout" element={
          <>
            <Navigation />
            <Checkout />
            <Footer />
          </>
        } />
        <Route path="/orders" element={
          <>
            <Navigation />
            <Orders />
            <Footer />
          </>
        } />
        <Route path="/orders/:orderId" element={
          <>
            <Navigation />
            <OrderDetail />
            <Footer />
          </>
        } />

        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>

        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/orders" element={<AdminOrders />} />
        <Route path="/admin/users" element={<AdminUsers />} />
        <Route path="/admin/products" element={<AdminProducts />} />
        <Route path="/admin/products/add" element={<AdminAddProduct />} />
        <Route path="/admin/categories" element={<AdminCategories />} />
        <Route path="/admin/categories/add" element={<AdminAddCategory />} />
        <Route path="/admin/categories/:categoryId/edit" element={<AdminEditCategory />} />
      </Routes>
    </div>
  );
}

export default App;
