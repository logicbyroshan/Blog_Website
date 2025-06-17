# ✍️ AI-Powered Blog & Portfolio Platform

![Django](https://img.shields.io/badge/Django-4.2-blue?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-blue?style=for-the-badge&logo=tailwindcss)
![TinyMCE](https://img.shields.io/badge/TinyMCE-6-blue?style=for-the-badge)

A modern, feature-rich blogging platform built with Django and a custom-themed admin panel for an exceptional content management experience. This project serves as a personal portfolio and a content hub, designed for performance, SEO, and ease of use.

## ✨ Features

This project isn't just a simple blog. It's a complete content management system with a focus on a clean user-facing design and a powerful, intuitive admin experience.

### Frontend (The Blog)
- **Responsive Design:** A beautiful, dark-themed interface built with Tailwind CSS that looks great on all devices.
- **Dynamic Content:** Serves blog posts, articles, categories, and author pages dynamically from the Django backend.
- **SEO Optimized:** Meta tags, descriptions, and clean URLs for every post.
- **User Engagement:** Features like post appreciations (likes) and a comment system.
- **Newsletter Subscription:** A dedicated section for users to subscribe to a newsletter.

### Custom Admin Panel (The Powerhouse)
- **Themed Interface:** A custom-built admin panel that matches the website's dark, modern aesthetic.
- **Comprehensive Dashboard:** At-a-glance statistics for published, scheduled, draft, and planned posts. Includes a dynamic performance chart and an editorial calendar.
- **Full Post Management:** A dedicated "Blogs List" page to view posts by status (Published, Scheduled, Draft).
- **In-line Actions:** Activate/deactivate posts on the site, edit, and delete directly from the list view.
- **Rich Text Editor:** Uses **TinyMCE** for a best-in-class, WYSIWYG blog writing experience.
- **Content Workflow:** Publish immediately, save as a draft, or schedule posts for a future date.
- **Activity Hub:** A centralized page to manage all comments (pin, delete) and view registered users and newsletter subscribers.
- **AI-Ready:** UI elements and backend hooks are in place for future integration of AI-powered tag generation and smart scheduling.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Python](https://www.python.org/downloads/) (version 3.9 or higher recommended)
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
- [Git](https://git-scm.com/downloads/) (for version control)

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/portfolio-project.git
    cd portfolio-project
    ```

2.  **Create and Activate a Virtual Environment**
    It's highly recommended to use a virtual environment to keep project dependencies isolated.

    *On Windows:*
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    *On macOS/Linux:*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    A `requirements.txt` file helps manage dependencies. Let's create one first (if you haven't already).

    *To generate the file from your current environment:*
    ```bash
    pip freeze > requirements.txt
    ```

    *To install from the file:*
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Key dependencies will include `Django`, `Pillow` for image handling, etc.)*

4.  **Set Up Environment Variables**
    Create a `.env` file in the project root directory. This file will hold your secret keys and other sensitive information.
    ```
    SECRET_KEY='your-strong-django-secret-key'
    DEBUG=True
    TINYMCE_API_KEY='your-free-api-key-from-tiny.cloud'
    ```

5.  **Apply Database Migrations**
    This will create the necessary database tables based on your `models.py` files.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a Superuser**
    This will be your administrator account to access the custom admin panel.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your username, email, and password.

7.  **Mark the Superuser as Staff**
    To access our custom admin panel (which is protected by the `@user_passes_test(is_staff)` decorator), you need to set the "staff status" for your new user.
    - Run the server: `python manage.py runserver`
    - Go to `http://127.0.0.1:8000/django-admin/`
    - Log in with your superuser credentials.
    - Go to "Users", click on your username, and check the **"Staff status"** box. Save the user.

8.  **Run the Development Server**
    You're all set!
    ```bash
    python manage.py runserver
    ```
    - Your blog will be available at `http://127.0.0.1:8000/`
    - Your custom admin panel will be at `http://127.0.0.1:8000/admin/`

---

## 📂 Project Structure

The project follows a standard Django structure with a focus on modular apps.

PORTFOLIO_PROJECT/
├── admin_app/ # Handles the custom admin panel
│ ├── migrations/
│ ├── static/ # CSS for the admin panel
│ ├── templates/ # HTML templates for the admin panel
│ │ └── admin_app/
│ │ ├── includes/ # Reusable template parts (e.g., sidebar.html)
│ │ ├── base.html
│ │ ├── admin-dash.html
│ │ └── ...
│ ├── urls.py
│ └── views.py
├── blog_app/ # Handles the public-facing blog
│ └── ... (models.py, views.py, etc.)
├── config/ # Main project configuration
│ ├── settings.py
│ └── urls.py
├── venv/ # Virtual environment (ignored by .gitignore)
├── .gitignore
├── db.sqlite3
└── manage.py


---

## 🧪 Running Tests

To run the test suite for the project, use the following command:

```bash
python manage.py test