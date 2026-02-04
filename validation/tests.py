from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Student
from .forms import StudentForm


class StudentModelTest(TestCase):
    """Tests for the Student model"""

    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 20,
            'grade': 8.5,
            'enrollment_date': date.today(),
            'is_active': True
        }

    def test_create_valid_student(self):
        """Test creating a student with valid data"""
        student = Student.objects.create(**self.valid_data)
        self.assertEqual(student.name, 'John Doe')
        self.assertEqual(student.email, 'john@example.com')
        self.assertEqual(student.age, 20)
        self.assertEqual(student.grade, 8.5)

    def test_student_str_method(self):
        """Test the __str__ method"""
        student = Student.objects.create(**self.valid_data)
        expected_str = f"{student.name} ({student.email})"
        self.assertEqual(str(student), expected_str)

    def test_name_too_short(self):
        """Test that name must be at least 2 characters"""
        self.valid_data['name'] = 'A'
        student = Student(**self.valid_data)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_age_below_minimum(self):
        """Test that age cannot be below 15"""
        self.valid_data['age'] = 14
        student = Student(**self.valid_data)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_age_above_maximum(self):
        """Test that age cannot exceed 100"""
        self.valid_data['age'] = 101
        student = Student(**self.valid_data)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_grade_below_minimum(self):
        """Test that grade cannot be negative"""
        self.valid_data['grade'] = -0.5
        student = Student(**self.valid_data)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_grade_above_maximum(self):
        """Test that grade cannot exceed 10.0"""
        self.valid_data['grade'] = 10.5
        student = Student(**self.valid_data)
        with self.assertRaises(ValidationError):
            student.full_clean()


class StudentFormTest(TestCase):
    """Tests for the StudentForm"""

    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'age': 22,
            'grade': 9.0,
            'enrollment_date': date.today(),
            'is_active': True
        }

    def test_valid_form(self):
        """Test form with valid data"""
        form = StudentForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_name_without_space(self):
        """Test that name must contain first and last name"""
        self.valid_data['name'] = 'SingleName'
        form = StudentForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_name_with_numbers(self):
        """Test that name cannot contain numbers"""
        self.valid_data['name'] = 'John 123'
        form = StudentForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_email(self):
        """Test that email must be unique"""
        Student.objects.create(**self.valid_data)
        form = StudentForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_future_enrollment_date(self):
        """Test that enrollment date cannot be in the future"""
        self.valid_data['enrollment_date'] = date.today() + timedelta(days=1)
        form = StudentForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('enrollment_date', form.errors)

    def test_cross_field_validation(self):
        """Test cross-field validation: age < 18 and grade > 8.0"""
        self.valid_data['age'] = 17
        self.valid_data['grade'] = 9.0
        form = StudentForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_cross_field_validation_passes(self):
        """Test cross-field validation passes when valid"""
        self.valid_data['age'] = 17
        self.valid_data['grade'] = 7.5
        form = StudentForm(data=self.valid_data)
        self.assertTrue(form.is_valid())


class StudentViewTest(TestCase):
    """Tests for the Student views"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.list_url = reverse('student-list')
        self.create_url = reverse('student-create')
        
        self.student_data = {
            'name': 'Test Student',
            'email': 'test@example.com',
            'age': 20,
            'grade': 8.5,
            'enrollment_date': date.today(),
            'is_active': True
        }
        
        self.student = Student.objects.create(**self.student_data)

    def test_list_view(self):
        """Test the student list view"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validation/student_list.html')
        self.assertContains(response, self.student.name)

    def test_create_view_get(self):
        """Test GET request to create view"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validation/student_form.html')

    def test_create_view_post_valid(self):
        """Test POST request with valid data"""
        new_data = {
            'name': 'New Student',
            'email': 'new@example.com',
            'age': 25,
            'grade': 7.0,
            'enrollment_date': date.today().isoformat(),
            'is_active': True
        }
        response = self.client.post(self.create_url, data=new_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Student.objects.filter(email='new@example.com').exists())

    def test_create_view_post_invalid(self):
        """Test POST request with invalid data"""
        invalid_data = {
            'name': 'N',  # Too short
            'email': 'invalid-email',
            'age': 10,  # Below minimum
            'grade': 15,  # Above maximum
            'enrollment_date': date.today().isoformat(),
        }
        response = self.client.post(self.create_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Stay on form page
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)

    def test_update_view_get(self):
        """Test GET request to update view"""
        update_url = reverse('student-update', kwargs={'pk': self.student.pk})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validation/student_form.html')

    def test_update_view_post_valid(self):
        """Test POST request to update with valid data"""
        update_url = reverse('student-update', kwargs={'pk': self.student.pk})
        updated_data = {
            'name': 'Updated Student',
            'email': self.student.email,
            'age': 30,
            'grade': 9.5,
            'enrollment_date': self.student.enrollment_date.isoformat(),
            'is_active': False
        }
        response = self.client.post(update_url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Updated Student')
        self.assertEqual(self.student.age, 30)

    def test_delete_view_get(self):
        """Test GET request to delete view"""
        delete_url = reverse('student-delete', kwargs={'pk': self.student.pk})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validation/student_confirm_delete.html')

    def test_delete_view_post(self):
        """Test POST request to delete"""
        delete_url = reverse('student-delete', kwargs={'pk': self.student.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

