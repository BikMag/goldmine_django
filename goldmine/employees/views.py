from django.shortcuts import render

from .models import EmployeesView


def employee_list(request):
    template_name = 'employees/employee_list.html'

    employees = EmployeesView.objects.all()

    context = {'employees': employees}

    return render(request, template_name, context)
