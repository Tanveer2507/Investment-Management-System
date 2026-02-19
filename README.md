# Investment Management System

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Tanveer2507/Investment-Management-System)
[![Website](https://img.shields.io/badge/Website-Live-green)](https://your-website-url.com)

A comprehensive investment management platform built with Django for tracking startups, investments, and portfolio management.

## 🌐 Live Demo

**Website:** [https://your-website-url.com](https://your-website-url.com)

## 🚀 Features

- **Startup Management**: Register and track startups
- **Investment Tracking**: Record and monitor investments
- **Portfolio Dashboard**: View comprehensive investment portfolio
- **Document Management**: Upload and manage investment documents
- **Watchlist**: Track interesting startups
- **Reports**: Generate investment and startup reports
- **User Authentication**: Secure login and registration
- **Settings**: Customizable user preferences
- **Newsletter**: Subscribe to updates

## 📋 Requirements

- Python 3.8+
- Django 5.0+
- SQLite (default) or PostgreSQL

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Tanveer2507/Investment-Management-System.git
cd Investment-Management-System
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Open browser and visit: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
Investment-Management-System/
├── core/                   # Main application
├── investment_system/      # Project settings
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── media/                # User uploads
├── scripts/              # Utility scripts
├── manage.py            # Django management
└── requirements.txt     # Dependencies
```

## 🎯 Usage

1. **Register/Login**: Create an account or login
2. **Browse Startups**: View available startups
3. **Add to Watchlist**: Track interesting startups
4. **Make Investment**: Record your investments
5. **View Dashboard**: Monitor your portfolio
6. **Generate Reports**: Analyze your investments

## 🔧 Configuration

Update settings in `investment_system/settings.py`:
- Database configuration
- Email settings
- Static files
- Media files

## 📧 Contact

For questions or support, please contact:
- **Email**: support@investtrack.com
- **GitHub**: [Tanveer2507](https://github.com/Tanveer2507)

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with Django and Bootstrap for a modern, responsive experience.
