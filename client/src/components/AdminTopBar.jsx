import React from 'react';
import { useNavigate } from 'react-router-dom';

const AdminTopBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/admin/login');
  };

  return (
    <div className="bg-white shadow-sm border-b border-gray-200 fixed top-0 left-64 right-0 z-10 h-16 flex items-center justify-between px-6">
      <div className="flex-1">
        {/* Breadcrumb or page title can go here */}
      </div>

      <div className="flex items-center space-x-4">
        <div className="text-sm text-gray-600">
          Welcome, Admin
        </div>

        <button
          onClick={handleLogout}
          className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors text-sm font-medium"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default AdminTopBar;
