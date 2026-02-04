from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age', 'grade', 'enrollment_date', 'is_active']
    list_filter = ['is_active', 'enrollment_date']
    search_fields = ['name', 'email']
    date_hierarchy = 'enrollment_date'
    ordering = ['-enrollment_date']

