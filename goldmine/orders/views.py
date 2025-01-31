from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.timezone import now
from .models import Customer, Employee, GoldOrder, OrderStates
from .forms import OrderStatusAndManagerForm, CreateOrderForm


def order_list(request):
    template_name = 'orders/order_list.html'

    gold_order_list = GoldOrder.objects.values(
        'order_id',
        'customer__last_name',
        'gold_amount',
        'ordering_date',
        'deadline',
        'status__name',
    )

    group = request.user.groups.all()[0].name
    if group == 'Заказчик':
        customer = Customer.objects.get(
            phone_number=request.user.phone_number
        )
        gold_order_list = gold_order_list.filter(customer=customer)
    elif group == 'Менеджер':
        employee = Employee.objects.get(
            phone_number=request.user.phone_number
        )
        gold_order_list = gold_order_list.filter(
            Q(employee=employee) | Q(employee=None)
        )

    context = {
        'order_list': gold_order_list,
    }

    return render(request, template_name, context)


def order_info(request, pk: int):
    template_name = 'orders/order_info.html'

    gold_order = GoldOrder.objects.get(order_id=pk)
    print(pk)
    print(GoldOrder.objects.all().get(order_id=pk))

    context = {
        'order': gold_order,
    }

    return render(request, template_name, context)


def create_order(request):
    template_name = 'orders/create_order.html'

    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            # Создаем объект заказа, но пока не сохраняем его в базу
            new_order = form.save(commit=False)

            customer = Customer.objects.get(
                phone_number=request.user.phone_number)

            # Устанавливаем автоматические значения
            new_order.customer = customer  # Текущий пользователь как заказчик
            new_order.ordering_date = now()   # Текущая дата
            new_order.status = OrderStates.objects.get(
                name='Оформлен')  # Статус "Оформлен"
            new_order.employee = None  # Менеджер не назначен

            # Сохраняем заказ
            new_order.save()

            # Уведомление об успешном добавлении
            # Перенаправляем на страницу заказа
            return redirect('orders:order_info', pk=new_order.pk)
    else:
        form = CreateOrderForm()

    context = {'form': form}

    return render(request, template_name, context)


def cancel_order(request, pk: int):
    template_name = 'orders/cancel_order.html'

    gold_order = get_object_or_404(GoldOrder, pk=pk)

    # Логика отмены заказа
    group = request.user.groups.all()[0].name
    if (
        group in ['Менеджер', 'Администратор']
        and gold_order.status.name in ['Отменен', 'Выполнено', 'Получено']
    ):
        message = ('Заказ нельзя отменить. '
                   + 'Он уже отменен или завершен.')
    elif (
        group == 'Заказчик'
        and gold_order.status.name not in ['Оформлен', 'Принят']
    ):
        message = ('Заказ нельзя отменить. '
                   + 'Он уже отменен, выполняется или завершен.')
    else:
        canceled_status = get_object_or_404(OrderStates, name='Отменен')
        gold_order.status = canceled_status
        gold_order.save()

        # Уведомляем об успешной отмене
        message = 'Заказ успешно отменен.'

    context = {
        'message': message,
    }

    return render(request, template_name, context)


def delete_order(request, pk):
    template_name = 'orders/delete_order.html'
    order = get_object_or_404(GoldOrder, order_id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('orders:order_list')

    context = {'order': order}

    return render(request, template_name, context)


def manager_change_order(request, pk: int):
    template_name = 'orders/manager_change_order.html'

    # Получаем заказ или возвращаем 404
    order = get_object_or_404(GoldOrder, pk=pk)

    if request.method == 'POST':
        form = OrderStatusAndManagerForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            new_status = form.cleaned_data['status']
            new_manager = form.cleaned_data['manager']

            # Обновляем статус и менеджера заказа
            order.status = new_status
            order.employee = new_manager
            order.save()

            # Возвращаемся на страницу заказа
            return redirect('orders:order_info', pk=order.pk)
    else:
        # Отображаем форму с начальными значениями
        try:
            manager = order.employee
        except Exception:
            manager = '-'

        form = OrderStatusAndManagerForm(
            initial={'status': order.status, 'manager': manager}
        )

    context = {'form': form, 'order': order}

    return render(request, template_name, context)
