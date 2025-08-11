# Student Payment Management System

A comprehensive Django-based web application for managing student payments and academic records. This system is designed for educational institutions to track student enrollment, monthly fees, and payment status across different grade levels.

## Features

### Core Functionality

- **Student Management**: Add, update, and delete student records
- **Grade-based Organization**: Support for grades 7-12 (الصف الأول الإعدادي to الصف الثالث الثانوي)
- **Payment Tracking**: Monthly payment management for the academic year (August to June)
- **Dashboard Analytics**: Real-time statistics and revenue tracking
- **Export Capabilities**: CSV export for student data and payment reports

### Key Features

- **Multi-language Support**: Arabic interface with RTL support
- **Payment Status Tracking**: Visual indicators for paid/unpaid/partial payments
- **Revenue Analytics**: Monthly and grade-wise revenue reporting
- **Search & Filter**: Advanced filtering by grade, payment status, and search terms
- **Responsive Design**: Mobile-friendly interface
- **Data Export**: CSV export with proper Arabic encoding

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker & Docker Compose
- **Web Server**: Gunicorn

## Project Structure

```
├── core/                   # Main Django app
│   ├── models.py          # Database models (Student, Grade, Payment)
│   ├── views.py           # Business logic and API endpoints
│   ├── forms.py           # Django forms
│   ├── admin.py           # Django admin configuration
│   ├── urls.py            # URL routing
│   └── migrations/        # Database migrations
├── src/                   # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── core/              # App-specific templates
├── static/                # Static files (CSS, JS, images)
├── staticfiles/           # Collected static files
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
└── manage.py             # Django management script
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd student-payment-system
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**

   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**

   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   The application will be available at `http://localhost:8000`

2. **Run migrations in Docker**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

## Usage Guide

### Initial Setup

1. **Access the application** at `http://localhost:8000`
2. **Create grade levels** through Django admin or by running:
   ```bash
   python manage.py shell
   ```
   Then execute:
   ```python
   from core.models import Grade
   grades = [
       ('grade7', 'الصف الأول الإعدادي'),
       ('grade8', 'الصف الثاني الإعدادي'),
       ('grade9', 'الصف الثالث الإعدادي'),
       ('grade10', 'الصف الأول الثانوي'),
       ('grade11', 'الصف الثاني الثانوي'),
       ('grade12', 'الصف الثالث الثانوي'),
   ]
   for grade_code, grade_name in grades:
       Grade.objects.get_or_create(grade=grade_code, defaults={'monthly_fee': 500.00})
   ```

### Main Workflows

1. **Dashboard**: View overall statistics and revenue summaries
2. **Grade Selection**: Choose specific grades to manage
3. **Student Management**: Add, edit, or remove student records
4. **Payment Tracking**: Update monthly payment status for students
5. **Reports**: Export data and generate payment reports

## Database Models

### Grade Model

- Stores grade levels (7-12) with Arabic names
- Configurable monthly fees per grade
- Unique grade identifiers

### Student Model

- Student personal information (name, phone, grade)
- Exemption status for special cases
- Automatic timestamp tracking

### Payment Model

- Monthly payment records (August to June)
- Payment status and amount tracking
- Automatic fee calculation based on grade
- Unique constraint per student/month/year

## API Endpoints

### AJAX Endpoints

- `GET /api/dashboard-stats/` - Dashboard statistics
- `POST /api/update-payment/` - Update payment status
- `GET /api/monthly-revenue/` - Monthly revenue data

### Export Endpoints

- `GET /export/students-csv/` - Export student data as CSV

## Configuration

### Environment Variables

- `DJANGO_SECRET_KEY`: Django secret key for security
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Settings Customization

Key settings in `src/settings.py`:

- Database configuration
- Static files handling
- Template directories
- Installed apps

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin

Access admin interface at `/admin/` with superuser credentials.

## Deployment

### Production Considerations

1. **Security**: Update `SECRET_KEY` and set `DEBUG=False`
2. **Database**: Use PostgreSQL for production
3. **Static Files**: Configure proper static file serving
4. **HTTPS**: Enable SSL/TLS encryption
5. **Backup**: Implement regular database backups

### Docker Production Deployment

```bash
# Build production image
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review existing issues for solutions

## Changelog

### Version 1.0.0

- Initial release
- Student and payment management
- Dashboard analytics
- CSV export functionality
- Docker support
- Arabic language interface
