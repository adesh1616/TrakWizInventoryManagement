# TrakWizInventoryManagement

# Online Product Management and Sales Platform

## Overview

This project is an online platform for managing products, selling them, and generating reports. It provides a centralized system for businesses to track product inventory, manage sales transactions, and analyze sales data.

## Features

## Screenshot
nmain page
![Screenshot 2024-04-11 130836](https://github.com/adesh1616/TrakWizInventoryManagement/assets/125434369/504960de-e32f-489b-939e-df21e49be6bc)

### Product Management

- **Add Product**: Users can add new products to the inventory, including product details such as name, description, price, and quantity.
- **Update Product**: Users can edit existing product details, such as price, quantity, and availability.
- **Delete Product**: Users can remove products from the inventory if they are no longer available.
- **Product Categories**: Products can be organized into different categories or departments for easier management and navigation.

### Sales Management

- **Sell Product**: Users can create sales transactions by selling products to customers. They can select products from the inventory, specify quantities, and generate invoices or receipts.
- **View Sales History**: Users can view a history of past sales transactions, including details such as product sold, quantity, customer information, and transaction date.
- **Order Fulfillment**: Users can track the status of sales orders, including pending orders, fulfilled orders, and cancelled orders.

### Reporting and Analytics

- **Sales Reports**: Generate reports on sales performance, including total sales revenue, top-selling products, sales trends over time, and sales by category.
- **Inventory Reports**: Generate reports on inventory status, including current stock levels, low stock alerts, out-of-stock items, and inventory turnover rates.
- **Customizable Reports**: Users can customize reports based on specific criteria, such as date range, product category, or sales channel.
- **Export Reports**: Reports can be exported in various formats (e.g., PDF, CSV) for further analysis or sharing with stakeholders.

### User Authentication and Authorization

- **User Authentication**: Implement user authentication to ensure secure access to the platform. Users must log in with their credentials to access the system.
- **Role-based Access Control**: Implement role-based access control (RBAC) to manage user permissions. Different user roles (e.g., admin, manager, staff) have different levels of access to features and data.

## Technologies Used

- **Frontend**: React.js, Redux (for state management), Material-UI (for UI components), Axios (for API requests).
- **Backend**: FastAPI (Python), PostgreSQL database, SQLAlchemy (for ORM), JWT authentication.
- **API Documentation**: Swagger UI (for interactive API documentation).
- **Deployment**: Docker (for containerization), Docker Compose (for multi-container deployment), NGINX (for reverse proxy), AWS or Heroku (for cloud hosting).

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:

```bash
git clone <repository-url>
cd online-product-management
```

2. Set up the backend:

- Create a virtual environment and activate it:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Set up the PostgreSQL database and configure the connection in the backend `.env` file.

- Run database migrations to create the necessary tables:

```bash
alembic upgrade head
```

- Start the backend server:

```bash
uvicorn main:app --reload
```

3. Set up the frontend:

Install node from: https://nodejs.org/en/download
Install Extension in VS code: npm Intellisense


```bash
Run `npm init react-app <your_module_name>`
Run `npm install bulma moment`
```

```bash
cd frontend
npm install
npm start
```

4. Access the application:

Open your web browser and navigate to `http://localhost:3000` to access the frontend of the application.
