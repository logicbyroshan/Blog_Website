# ✍️ AI-Powered Blog & Portfolio Platform

![Django](https://img.shields.io/badge/Django-4.2-blue?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-blue?style=for-the-badge&logo=tailwindcss)
![TinyMCE](https://img.shields.io/badge/TinyMCE-6-blue?style=for-the-badge)

A modern, AI-ready blogging platform built with Django, featuring a **custom admin dashboard**, **SEO-optimized frontend**, and integration hooks for future enhancements like AI content assistance and smart post scheduling. Designed for creators, developers, and portfolio showcases.

---

## ✨ Features

### 📰 Blog Frontend
- **Responsive Design** with Tailwind CSS.
- **Dynamic Content** rendered from Django DB (posts, categories, authors).
- **SEO-Friendly** with clean URLs and meta descriptions.
- **User Interaction**: Likes, Comments, and Newsletter Signups.
- **Dark Mode** theme with smooth UI transitions.

### 🛠️ Custom Admin Dashboard
- **Modern UI** consistent with frontend dark theme.
- **Post Workflow**: Drafts, Scheduled, and Published states.
- **Powerful Dashboard** with charts, stats, and editorial calendar.
- **Rich Text Editor** using **TinyMCE** (WYSIWYG).
- **Quick Actions**: Pin/unpin comments, publish in-line, and tag posts.
- **AI-Integration Ready** for smart tags and scheduling logic.

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.9+
- pip
- Git

### ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/portfolio-project.git
cd portfolio-project

# Create a virtual environment
python -m venv venv
# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 🔐 Environment Setup

Create a `.env` file in the root folder with:

```env
SECRET_KEY='your-django-secret-key'
DEBUG=True
TINYMCE_API_KEY='your-tinymce-key'
```

### 🛠️ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 👤 Create Superuser

```bash
python manage.py createsuperuser
# Then visit http://127.0.0.1:8000/django-admin to mark "staff" status
```

### ▶️ Run Development Server

```bash
python manage.py runserver
```

- Visit frontend: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

## 📂 Project Structure

The project follows a modular Django structure:

```text
PORTFOLIO_PROJECT/
├── admin_app/                  # Custom admin panel logic
│   ├── migrations/             # Django migrations
│   ├── static/                 # CSS, JS, images for admin
│   ├── templates/              # HTML templates for admin
│   │   └── admin_app/
│   │       ├── includes/       # Reusable components (sidebar, navbar)
│   │       ├── base.html       # Main admin layout
│   │       └── admin-dash.html # Dashboard view
│   ├── urls.py
│   └── views.py
│
├── blog_app/                   # Public-facing blog logic
│   ├── migrations/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   └── models.py
│
├── config/                     # Project settings and URLs
│   ├── settings.py
│   └── urls.py
│
├── venv/                       # Python virtual environment
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
└── .gitignore                  # Git ignore rules
```

---

## 🔮 Future Enhancements

- 🤖 AI-generated tags using NLP
- 🧠 Smart scheduling suggestions based on engagement data
- 📈 Admin analytics using Chart.js or Recharts
- 🌐 Multilingual support
- 🔒 Two-factor authentication for admin login

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 💡 Contributing

Contributions, issues, and feature requests are welcome!

```bash
# Fork the repository
# Create your feature branch: git checkout -b feature/yourFeature
# Commit your changes: git commit -m 'Add some feature'
# Push to the branch: git push origin feature/yourFeature
# Open a pull request 🚀
```

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🙌 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [TinyMCE](https://www.tiny.cloud/)
- OpenAI for AI inspiration
- AI Studio for Code Genration