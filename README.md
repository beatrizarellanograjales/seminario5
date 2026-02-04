# seminario5
data_seminario5

## Data Validation Class View - Django Implementation

This project demonstrates comprehensive data validation using Django class-based views.

### Features

- **Django Class-Based Views** for CRUD operations
- **Model-level validation** with custom validators
- **Form-level validation** with cross-field validation
- **Bootstrap-styled templates** with error display
- **Comprehensive test suite** with 22 tests

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Access the application at:
   - Student list: http://localhost:8000/students/
   - Admin panel: http://localhost:8000/admin/

### Data Validation Rules

The Student model includes the following validation rules:

- **Name**: Minimum 2 characters, must contain first and last name, only letters and spaces
- **Email**: Must be valid email format and unique
- **Age**: Between 15 and 100
- **Grade**: Between 0.0 and 10.0
- **Enrollment Date**: Cannot be in the future or more than 50 years old
- **Cross-field validation**: Students under 18 cannot have a grade higher than 8.0

### Running Tests

Run the test suite:
```bash
python manage.py test validation
```

### Project Structure

```
seminario5/
├── data_seminario5/          # Main project settings
├── validation/               # Validation app
│   ├── models.py            # Student model with validators
│   ├── forms.py             # StudentForm with validation
│   ├── views.py             # Class-based views
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   ├── tests.py             # Comprehensive tests
│   └── templates/           # HTML templates
├── manage.py
└── requirements.txt
```

### Class-Based Views

- **StudentListView**: Display all students with pagination
- **StudentCreateView**: Create new student with validation
- **StudentUpdateView**: Update existing student with validation
- **StudentDeleteView**: Delete student with confirmation

