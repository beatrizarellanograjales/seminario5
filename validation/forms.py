from django import forms
from django.core.exceptions import ValidationError
from .models import Student
import datetime


class StudentForm(forms.ModelForm):
    """Form with comprehensive validation for Student model"""
    
    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'grade', 'enrollment_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@example.com'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '15',
                'max': '100'
            }),
            'grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '10'
            }),
            'enrollment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name')
        if name:
            # Check for at least one space (first and last name)
            if ' ' not in name.strip():
                raise ValidationError('Please enter both first and last name.')
            # Check for valid characters
            if not all(c.isalpha() or c.isspace() for c in name):
                raise ValidationError('Name should only contain letters and spaces.')
        return name
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (excluding current instance if editing)
            queryset = Student.objects.filter(email=email)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError('A student with this email already exists.')
        return email
    
    def clean_enrollment_date(self):
        """Validate enrollment date"""
        enrollment_date = self.cleaned_data.get('enrollment_date')
        if enrollment_date:
            # Enrollment date cannot be in the future
            if enrollment_date > datetime.date.today():
                raise ValidationError('Enrollment date cannot be in the future.')
            # Enrollment date cannot be too old (e.g., more than 50 years ago)
            min_date = datetime.date.today() - datetime.timedelta(days=365*50)
            if enrollment_date < min_date:
                raise ValidationError('Enrollment date is too old.')
        return enrollment_date
    
    def clean(self):
        """Form-level validation"""
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        grade = cleaned_data.get('grade')
        
        # Cross-field validation
        if age and grade:
            if age < 18 and grade > 8.0:
                raise ValidationError(
                    'Students under 18 cannot have a grade higher than 8.0'
                )
        
        return cleaned_data
