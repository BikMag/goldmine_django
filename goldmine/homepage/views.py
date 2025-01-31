from django.shortcuts import render
from django.db import connection
from homepage.admin import add_customer, add_employee
from orders.models import Customer, Employee


def index(request):
    template_name = 'homepage/index.html'
    if request.user.is_authenticated:
        phone = request.user.phone_number
        group = request.user.groups.all()[0].name

        if group == 'Заказчик':
            customer = Customer.objects.filter(phone_number=phone)
            if len(customer) == 0:
                add_customer(request.user)
        elif group in ['Менеджер', 'Рабочий']:
            customer = Employee.objects.filter(phone_number=phone)
            if len(customer) == 0:
                add_employee(request.user)

    with connection.cursor() as db:
        db.execute('SELECT CountManualGoldCost(41.35);')
        total_sum = db.fetchone()[0]

        db.callproc('most_active_employee')
        most_active_customer = ' '.join(db.fetchone()[1:3])

    context = {
        'total_sum': total_sum,
        'most_active_customer': most_active_customer,
    }

    return render(request, template_name, context)
