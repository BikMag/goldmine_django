from orders.models import Customer, Employee, Position


def add_customer(user: Customer):
    Customer.objects.create(
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def add_employee(user: Employee):
    position = Position.objects.get(name=user.groups.all()[0].name)
    Employee.objects.create(
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name,
        position=position
    )
