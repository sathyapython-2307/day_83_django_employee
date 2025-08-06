from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Employee

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'directory/employee_list.html'

    def get_queryset(self):
        dept_id = self.request.GET.get('department')
        if dept_id:
            return Employee.objects.filter(department_id=dept_id)
        return Employee.objects.all()

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'directory/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = f"Home > {self.object.department.name} > {self.object.name}"
        return context

class HRPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class EmployeeCreateView(LoginRequiredMixin, HRPermissionMixin, CreateView):
    model = Employee
    fields = ['name', 'email', 'phone', 'department']
    template_name = 'directory/employee_form.html'
    success_url = reverse_lazy('employee-list')

class EmployeeUpdateView(LoginRequiredMixin, HRPermissionMixin, UpdateView):
    model = Employee
    fields = ['name', 'email', 'phone', 'department']
    template_name = 'directory/employee_form.html'
    success_url = reverse_lazy('employee-list')

class EmployeeDeleteView(LoginRequiredMixin, HRPermissionMixin, DeleteView):
    model = Employee
    template_name = 'directory/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')
