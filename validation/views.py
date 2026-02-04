from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Student
from .forms import StudentForm


class StudentListView(ListView):
    """Class-based view to list all students"""
    model = Student
    template_name = 'validation/student_list.html'
    context_object_name = 'students'
    paginate_by = 10


class StudentCreateView(CreateView):
    """Class-based view to create a new student with validation"""
    model = Student
    form_class = StudentForm
    template_name = 'validation/student_form.html'
    success_url = reverse_lazy('student-list')
    
    def form_valid(self, form):
        """Called when form validation succeeds"""
        messages.success(self.request, 'Student created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Called when form validation fails"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class StudentUpdateView(UpdateView):
    """Class-based view to update a student with validation"""
    model = Student
    form_class = StudentForm
    template_name = 'validation/student_form.html'
    success_url = reverse_lazy('student-list')
    
    def form_valid(self, form):
        """Called when form validation succeeds"""
        messages.success(self.request, 'Student updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Called when form validation fails"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class StudentDeleteView(DeleteView):
    """Class-based view to delete a student"""
    model = Student
    template_name = 'validation/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')
    
    def post(self, request, *args, **kwargs):
        """Called when delete is confirmed"""
        messages.success(self.request, 'Student deleted successfully!')
        return super().post(request, *args, **kwargs)

