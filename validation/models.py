from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.core.exceptions import ValidationError

# Custom validator function
def validate_name_length(value):
    """Validate that name is at least 2 characters long"""
    if len(value) < 2:
        raise ValidationError(
            'Name must be at least 2 characters long.',
            params={'value': value},
        )

class Student(models.Model):
    """Student model with comprehensive data validation"""
    name = models.CharField(
        max_length=100,
        validators=[validate_name_length],
        help_text="Student's full name (minimum 2 characters)"
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Student's email address"
    )
    age = models.IntegerField(
        validators=[
            MinValueValidator(15, message="Student must be at least 15 years old"),
            MaxValueValidator(100, message="Age cannot exceed 100")
        ],
        help_text="Student's age (15-100)"
    )
    grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0, message="Grade cannot be negative"),
            MaxValueValidator(10.0, message="Grade cannot exceed 10.0")
        ],
        help_text="Student's grade (0.0-10.0)"
    )
    enrollment_date = models.DateField(
        help_text="Date of enrollment"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the student is currently active"
    )
    
    class Meta:
        ordering = ['-enrollment_date']
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def clean(self):
        """Model-level validation for cross-field validation rules"""
        super().clean()
        # Additional custom validation can be added here
        # Note: Field-level validation is handled by validators
    
    def __str__(self):
        return f"{self.name} ({self.email})"

