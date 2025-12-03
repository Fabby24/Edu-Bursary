"""
# 🎓 Edu Bursary Finder Platform

A comprehensive web platform built with Django and Bootstrap 5 that helps students discover, track, and apply for educational bursaries, scholarships, and grants across Africa.

## ✨ Features

### For Students
- **Smart Search & Filtering**: Find bursaries by category, location, education level, and field of study
- **Personalized Recommendations**: AI-powered matching based on student profile
- **Application Tracker**: Monitor application status from saved to approved
- **Document Management**: Upload and organize required documents
- **Bookmark System**: Save interesting opportunities for later
- **AI Chatbot Assistant**: Get instant help with finding bursaries and application guidance
- **Profile Management**: Complete academic profile for better matches

### For Administrators
- **Comprehensive Dashboard**: Real-time analytics and insights
- **Bursary Management**: Create, approve, and manage bursary listings
- **User Management**: Monitor and manage student accounts
- **Analytics & Reporting**: Charts, trends, and performance metrics
- **Export Functionality**: Download data as CSV for reporting
- **Activity Logging**: Track all admin actions for audit trail

## 🏗️ Technical Stack

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5.3, JavaScript ES6
- **Database**: PostgreSQL (production) / SQLite (development)
- **AI Integration**: Anthropic Claude / OpenAI GPT
- **Cache**: Redis (optional)
- **Static Files**: WhiteNoise
- **Charts**: Chart.js

## 📦 Project Structure

```
edu_bursary_platform/
├── config/                 # Project settings
├── apps/
│   ├── accounts/          # User authentication & profiles
│   ├── bursaries/         # Bursary listings & recommendations
│   ├── applications/      # Application tracking
│   ├── chatbot/           # AI chatbot integration
│   └── dashboard/         # Admin analytics
├── templates/             # HTML templates
├── static/                # CSS, JS, images
└── media/                 # User uploads
```

## 🚀 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL (or SQLite for development)
- pip and virtualenv

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd edu_bursary_platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=bursary_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

ANTHROPIC_API_KEY=your-claude-key
OPENAI_API_KEY=your-openai-key
CHATBOT_MODEL=claude
```

### AI Chatbot Setup

1. Get API key from [Google Ai studio](https://aistudio.google.com)
2. Add key to `.env` file
3. Set `CHATBOT_MODEL` to either `gemini-2.0 Flash`

The chatbot will:
- Search the database for relevant bursaries
- Use student profile for personalized responses
- Maintain conversation history
- Provide step-by-step application guidance

## 🎨 UI Customization

The platform uses a consistent color theme defined in `static/css/custom.css`:

- **Primary**: #1A73E8 (Blue)
- **Secondary**: #0C3B78 (Dark Blue)
- **Accent**: #F9A825 (Gold)
- **Background**: #F5F7FA (Light Gray)

To customize, edit the CSS variables in `custom.css`.

## 📊 Recommendation Algorithm

The system uses a multi-factor scoring algorithm (0-100):

1. **Profile Matching (40%)**: Education level, field, GPA, location
2. **Trending Score (20%)**: Views, bookmarks, applications
3. **Deadline Urgency (20%)**: Days until deadline
4. **Pattern Matching (20%)**: Similar user applications

Implementation: `apps/bursaries/recommendations.py`

## 🔐 Security Features

- CSRF protection on all forms
- User authentication required for sensitive actions
- File upload validation (type, size)
- SQL injection prevention (Django ORM)
- XSS protection (template auto-escaping)
- Secure password hashing (PBKDF2)
- HTTPS enforcement in production
- Environment variable for secrets

## 📱 Mobile Responsive

The platform is fully responsive and works seamlessly on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test apps.bursaries

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Query optimization with `select_related` and `prefetch_related`
- Static file compression with WhiteNoise
- Pagination for large result sets
- Redis caching (optional)
- CDN for Bootstrap and jQuery

## 🚢 Deployment

### Heroku
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
```

### DigitalOcean/VPS
See detailed guide in `requirements_deployment.txt`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file.

## 👥 Support

For issues and questions:
- Email: support@bursaryfinder.com
- GitHub Issues: [Create Issue](your-repo-url/issues)
- Documentation: [Wiki](your-repo-url/wiki)

## 🙏 Acknowledgments

- Bootstrap 5 for UI components
- Django framework
- Anthropic/OpenAI for AI capabilities
- Chart.js for visualizations
- All contributors

---

**Built with ❤️ for students across Africa**
"""