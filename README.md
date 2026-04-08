# 📸 Lensa - Gallery Web Application

> **The Digital Curator** — Temukan inspirasi visual terbaik dari fotografer di seluruh dunia.

---

## 🔗 Links

| Resource | URL |
|----------|-----|
| 🐙 **GitHub Repository** | [https://github.com/hajaww/Gallery-Web](https://github.com/hajaww/Gallery-Web) |
| 📁 **Google Drive** | [Dokumentasi & File](https://drive.google.com/drive/folders/1jkOsLT_NMfRLHpZtpzL_LCGsgTey4GtU?usp=drive_link) |

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Database Migration](#-database-migration)
- [API Routes](#-api-routes)
- [Author](#-author)

---

## 🎯 Overview

**Lensa** adalah aplikasi web galeri foto yang dibangun menggunakan **Flask** sebagai backend framework dengan **Tailwind CSS** untuk styling. Aplikasi ini memungkinkan pengguna untuk:

- Upload, edit, dan delete foto
- Like foto dengan sistem 1 user = 1 like
- Search foto berdasarkan judul, deskripsi, atau nama uploader
- Sorting foto berdasarkan **recent** atau **trending**
- Pagination untuk performa optimal
- Dark mode UI dengan glassmorphism design
- Rate limiting untuk keamanan

---

## 🛠 Tech Stack

### **Backend**
| Technology | Version | Description |
|------------|---------|-------------|
| [Python](https://www.python.org/) | 3.x | Programming language |
| [Flask](https://flask.palletsprojects.com/) | 3.0.0 | Web framework |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) | 3.1.1 | ORM untuk database |
| [Flask-Login](https://flask-login.readthedocs.io/) | 0.6.3 | User session management |
| [Flask-WTF](https://flask-wtf.readthedocs.io/) | 1.2.1 | Form handling & CSRF protection |
| [Flask-Migrate](https://flask-migrate.readthedocs.io/) | 4.0.5 | Database migration (Alembic) |
| [Flask-Limiter](https://flask-limiter.readthedocs.io/) | 3.5.0 | Rate limiting |
| [PyMySQL](https://pymysql.readthedocs.io/) | 1.1.0 | MySQL driver |

### **Frontend**
| Technology | Description |
|------------|-------------|
| [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS framework (CDN) |
| Google Fonts (Inter) | Typography |
| Material Icons Round | Icon library |
| Vanilla JavaScript | Interactivity & AJAX |

### **Database**
| Technology | Description |
|------------|-------------|
| MySQL | Database server |
| SQLAlchemy | ORM |

---

## ✨ Features

### 👤 Authentication
- ✅ Register dengan validasi password (min 8 karakter, huruf kapital, angka)
- ✅ Login dengan session management
- ✅ Logout dengan redirect
- ✅ Edit profil user

### 📸 Photo Management
- ✅ Upload foto (max 16MB) dengan validasi format
- ✅ Edit foto (title, description, replace image)
- ✅ Delete foto dengan file cleanup
- ✅ View foto per user dengan pagination

### 🎨 Gallery
- ✅ Grid layout responsive
- ✅ Pagination (12 foto per halaman)
- ✅ Sorting: **Recent** (terbaru) & **Trending** (most liked)
- ✅ Search by title, description, atau uploader name
- ✅ Download foto

### ❤️ Like System
- ✅ 1 User = 1 Like per foto (toggle)
- ✅ AJAX request (no page reload)
- ✅ Rate limiting (60 likes/minute)
- ✅ Hanya user yang sudah login bisa like

### 🔒 Security
- ✅ CSRF Protection
- ✅ Rate Limiting (200/day, 50/hour default)
- ✅ Password hashing dengan Werkzeug
- ✅ File upload validation
- ✅ Error handling & logging

### 🎨 UI/UX
- ✅ Dark mode dengan custom color palette
- ✅ Glassmorphism design
- ✅ Responsive layout (mobile-friendly)
- ✅ Smooth animations & transitions
- ✅ Custom scrollbar
- ✅ Toast notifications (flash messages)

---

## 📁 Project Structure

```
Gallery-Web/
├── app.py                  # Main application & routes
├── config.py               # Configuration (database, upload, secret key)
├── models.py               # Database models (User, Photo, Like)
├── database.sql            # SQL schema dump
├── requirement.txt         # Python dependencies
├── .env.example            # Environment variables template
│
├── static/                 # Static files
│   ├── uploads/            # Uploaded photos
│   ├── lensa.png           # Logo
│   └── lensalogo.png       # Favicon
│
├── templates/              # Jinja2 templates
│   ├── base.html           # Base layout (navbar, footer, CSS)
│   ├── index.html          # Home/gallery page
│   ├── login.html          # Login page
│   ├── register.html       # Register page
│   ├── upload.html         # Upload/edit photo page
│   ├── my_photos.html      # User's photo dashboard
│   ├── edit_profile.html   # Edit profile page
│   └── components/         # Reusable components
│       └── _navbar.html    # Navigation bar
│
├── migrations/             # Database migrations (Alembic)
│   ├── alembic.ini
│   ├── env.py
│   └── versions/           # Migration scripts
│
└── venv/                   # Virtual environment (not tracked)
```

---

## 🚀 Installation

### **Prerequisites**
- Python 3.8+
- MySQL Server
- pip (Python package manager)
- Git

### **Step-by-Step**

1. **Clone repository**
```bash
git clone https://github.com/hajaww/Gallery-Web.git
cd Gallery-Web
```

2. **Buat virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirement.txt
```

4. **Setup database MySQL**
```bash
# Login ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE lensa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Konfigurasi environment**
```bash
# Copy file .env.example ke .env
cp .env.example .env

# Edit file .env dengan konfigurasi database kamu
```

6. **Jalankan migration**
```bash
flask db upgrade
```

7. **Jalankan aplikasi**
```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

---

## ⚙️ Configuration

### **Environment Variables** (`.env`)

Buat file `.env` di root project dengan konfigurasi berikut:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost/lensa_db

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp
```

> ⚠️ **Penting:** Jangan pernah commit file `.env` ke repository. Gunakan `.env.example` sebagai template.

### **Config.py**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/lensa_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,webp').split(','))
```

---

## 🗄 Database Migration

### **Alembic/Flask-Migrate Commands**

```bash
# Initialize migration (hanya sekali di awal)
flask db init

# Buat migration baru setelah perubahan models
flask db migrate -m "Deskripsi perubahan"

# Apply migration ke database
flask db upgrade

# Rollback migration
flask db downgrade

# Lihat riwayat migration
flask db history
```

---

## 🛣 API Routes

### **Public Routes**

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home/Gallery dengan pagination |
| GET | `/search?q=query` | Search foto |
| GET | `/download/<photo_id>` | Download foto |
| GET | `/login` | Login page |
| POST | `/login` | Login process |
| GET | `/register` | Register page |
| POST | `/register` | Register process |

### **Protected Routes** (Login Required)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/logout` | Logout |
| GET | `/upload` | Upload form |
| POST | `/upload` | Upload photo |
| GET | `/my-photos` | User's photo dashboard |
| GET | `/edit-profile` | Edit profile form |
| POST | `/edit-profile` | Update profile |
| GET | `/edit/<photo_id>` | Edit photo form |
| POST | `/edit/<photo_id>` | Update photo |
| POST | `/delete/<photo_id>` | Delete photo |
| POST | `/like/<photo_id>` | Like/unlike photo (AJAX) |

### **AJAX Endpoints**

| Method | Route | Response | Description |
|--------|-------|----------|-------------|
| POST | `/like/<photo_id>` | `{"likes": int, "liked": bool}` | Toggle like |

---

## 📊 Database Schema

### **Models**

```
User
├── id (Integer, PK)
├── name (String)
├── email (String, Unique)
├── password_hash (String)
├── created_at (DateTime)
└── photos, likes (Relationships)

Photo
├── id (Integer, PK)
├── title (String)
├── description (Text)
├── image_file (String)
├── user_id (Integer, FK -> User.id)
├── likes_count (Integer, Default: 0)
├── created_at (DateTime)
└── uploader, likes (Relationships)

Like
├── id (Integer, PK)
├── user_id (Integer, FK -> User.id)
├── photo_id (Integer, FK -> Photo.id)
└── user, photo (Relationships)
```

---

## 🧪 Testing

```bash
# Jalankan test (jika ada)
pytest

# Atau jalankan Flask test server
python app.py
```

---

## 📝 License

Project ini dibuat untuk keperluan pembelajaran. © 2026 oleh Faeyza SMK 2 Cimahi.

---

## 👨‍💻 Author

**Faeyza** — SMK 2 Cimahi

- GitHub: [hajaww](https://github.com/hajaww)
- Google Drive: [Project Files](https://drive.google.com/drive/folders/1jkOsLT_NMfRLHpZtpzL_LCGsgTey4GtU?usp=drive_link)

---

<div align="center">

**Made with ❤️ using Flask + Tailwind CSS**

⭐ Star this repository if you find it helpful!

</div>
