# Custom Dress Platform

A comprehensive Django-based web application that connects customers with professional dress designers. The platform facilitates the entire custom dressmaking process, from the initial design request and quotation to order tracking, payment, delivery, and post-delivery alterations.

## Features

### 1. User Roles & Profiles
*   **Customers**: Can browse designers, submit detailed dress requests, make payments, track orders, and leave reviews.
*   **Designers**: Maintain a professional profile (bio, specialties, price range, portfolio), manage incoming design requests, update order statuses, and receive reviews.
*   **Admins**: Oversee the platform, approve new designer accounts, and manage users.

### 2. Dress Requests System
Customers can submit highly detailed requests to specific designers, including:
*   **Dress Specifics**: Type (wedding, evening, casual, etc.), fabric preferences, neck type, hemline, and colors.
*   **Measurements**: Bust, waist, hips, height, sleeve length, and additional custom measurements.
*   **Logistics**: Budget constraints and desired completion deadlines.
*   **Inspiration**: Reference images and detailed descriptions.
Designers can review these requests, provide notes, quote a final price, and estimate a completion date.

### 3. Order Management & Tracking
Once a request is accepted and paid for, an order is generated.
*   **Lifecycle Tracking**: Orders move through a detailed status pipeline (`Pending` -> `Accepted` -> `Paid` -> `Tailoring` -> `Ready` -> `Shipping` -> `Delivered` -> `Done`).
*   **Alterations**: A 7-day alteration window opens automatically upon delivery, allowing customers to request adjustments before the order is marked as completely done.

### 4. Payments
*   Supports different payment methods including Credit/Debit Card and Cash on Delivery (COD).
*   Tracks payment status and links transactions securely to orders.

### 5. Messaging
*   Built-in threaded messaging system allowing direct communication between customers and designers.
*   Messages can be linked to specific dress requests or orders for context.
*   Supports attachments for sharing progress pictures or additional reference materials.

### 6. Reviews & Ratings
*   Customers can leave reviews (1-5 stars) and upload photos of the completed dress.
*   Designers have the ability to respond to reviews.
*   Automatically calculates and updates the designer's overall rating on their profile.

## Technology Stack

*   **Backend Framework**: Django 5.1.5
*   **Database**: SQLite (Default, configurable for production)
*   **Frontend**: HTML, CSS, Django Templates
*   **API**: Django REST Framework (Installed)

## Project Structure

The project is broken down into modular Django apps for clean architecture:
*   `dress_platform/`: Core project settings and URL routing.
*   `users/`: Custom `User` model handling authentication and role-based access.
*   `designers/`: Models for `DesignerProfile` and `DesignerDesign` (portfolio items).
*   `dress_requests/`: Models managing the initial design proposal phase.
*   `orders/`: Models for `Order` and `AlterationRequest`.
*   `payments/`: Payment tracking and transaction history.
*   `messaging/`: In-app communication system.
*   `reviews/`: Feedback and rating system.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv311
    # On Windows:
    venv311\Scripts\activate
    # On macOS/Linux:
    source venv311/bin/activate
    ```

3.  **Install dependencies:**
    *(Assuming a `requirements.txt` is present)*
    ```bash
    pip install -r requirements.txt
    ```
    *If no requirements file is present, you can install the core dependencies manually:*
    ```bash
    pip install django djangorestframework pillow
    ```

4.  **Run database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/`.


