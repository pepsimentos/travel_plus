# **Travelo - Travel Agency Management System**

Travelo is a comprehensive travel management system designed to facilitate flight, hotel, and vacation package bookings. The platform supports two types of users: **agents** and **clients**. Agents can manage vacation packages for clients, while clients can browse and request bookings via the agents.

---

## **Table of Contents**
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Dummy Data Generation](#dummy-data-generation)
- [Running the Project](#running-the-project)
- [Workflow](#workflow)
  - [User Workflows](#user-workflows)
  - [Agent Workflows](#agent-workflows)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## **Features**
- User-friendly interface for agents and clients.
- Centralized management of vacation packages.
- Live booking system for flights and hotels.
- Support for agent-specific vacation package bookings.
- Client redirection to agents for personalized vacation plans.

---

## **Technologies Used**
- **Backend**: Django 5.1.3
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3
- **Environment Management**: Virtualenv
- **Scripts**: Custom management commands for dummy data generation

---

## **Getting Started**

### **Prerequisites**
Ensure the following software is installed on your system:
- Python (>= 3.12)
- Virtualenv (`pip install virtualenv`)
- SQLite3 (pre-installed with Python)

### **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/travelo.git
   cd travelo
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv travelo
   source travelo/bin/activate  # On Windows: travelo\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### **Database Setup**
1. Apply migrations to set up the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

### **Dummy Data Generation**
Generate dummy data for flights and hotels using the provided scripts.

1. **Flights**:
   ```bash
   python manage.py generate_flights
   ```
   
2. **Hotels**:
   ```bash
   python manage.py generate_hotels
   ```

---

## **Running the Project**
Start the development server:
```bash
python manage.py runserver
```
Visit the application in your browser at `http://127.0.0.1:8000`.

---

## **Workflow**

### **User Workflows**
1. **Login/Register**: 
   - Users can log in or register through the authentication system.
2. **Browse Packages**: 
   - View available vacation packages and package details.
3. **Request Bookings**: 
   - Redirected to agents to facilitate vacation package bookings.
4. **Flight and Hotel Search**: 
   - Search for available flights or hotels for specific destinations.

### **Agent Workflows**
1. **Login**: 
   - Agents log in with pre-registered credentials (created via admin panel).
2. **Package Management**: 
   - Add, edit, and manage vacation packages.
3. **Booking Management**: 
   - Assign packages to users and manage booking statuses.
4. **Capacity Management**: 
   - Flights and hotel capacities are dynamically updated upon booking.

---

## **Project Structure**
```
Travelo/
├── manage.py                  # Django project entry point
├── db.sqlite3                 # SQLite3 database
├── requirements.txt           # Python dependencies
├── travelo/                   # Django project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Project-wide URL routing
│   ├── wsgi.py                # WSGI application entry point
├── users/                     # Core app for managing users, agents, bookings
│   ├── models.py              # Database models
│   ├── views.py               # Application logic
│   ├── templates/             # HTML templates
│   │   ├── users/             # Templates for users app
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── navbar.html
│   ├── static/                # CSS, JS, and images
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   ├── admin.py               # Admin configurations
│   ├── management/            # Custom management commands
│       ├── commands/
│           ├── generate_flights.py
│           ├── generate_hotels.py
```

---

## **Contributing**
Contributions are welcome! Follow the steps below:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature-name'`.
4. Push to your branch: `git push origin feature-name`.
5. Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
