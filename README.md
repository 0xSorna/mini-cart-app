# Ecommerce MVP

A simple ecommerce minimum viable product (MVP) built for college project to practice Flask backend and basic React frontend development.

## Tech Stack

### Backend

- **Flask** - Lightweight WSGI web application framework
- **SQLAlchemy** - Python SQL toolkit and Object-Relational Mapping
- **Flask-JWT-Extended** - JWT authentication extension for Flask
- **SQLite** - Database engine

### Frontend

- **React** - JavaScript library for building user interfaces
- **Axios** - HTTP client for making API requests
- **CSS** - Styling and layout

## Project Structure

```
ecom-project/
├── backend/          # Flask API server
│   ├── main.py      # Main Flask application
│   ├── JUSTFILE     # Just commands for development
│   ├── requirements.txt # Python dependencies
│   └── src/         # Source code
│       ├── models.py # Database models
│       └── routes.py # API endpoints
└── client/          # React frontend (if exists)
    └── ...         # Frontend code
```

## Quick Start

### Backend

```bash
cd backend
just install    # Install dependencies
just run        # Start Flask development server
just freeze     # Update requirements.txt
```

### Frontend (when available)

```bash
cd client
npm install     # Install dependencies
npm run dev     # Start development server
```

## Features

- User authentication with JWT
- Admin panel for product management
- Basic ecommerce functionality
- Responsive UI with CSS

## Development Goals

This project serves as a learning exercise to understand:

- Flask application structure and routing
- Database modeling with SQLAlchemy
- JWT authentication implementation
- Basic React component development
- HTTP client usage with Axios
- Full-stack web development workflow
