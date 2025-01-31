from django.shortcuts import get_object_or_404, render, redirect
from orders.models import GoldOrder
from tasks.forms import TaskForm
from tasks.models import Tasks


def task_list(request):
    template_name = 'tasks/task_list.html'

    phone_number = request.user.phone_number
    tasks = Tasks.objects.values(
        'id',
        'gold_order__order_id',
        'step',
        'gold_order__deadline',
        'description',
        'completed',
    ).filter(
        worker__phone_number=phone_number
    ).order_by('completed', '-gold_order__deadline', 'step')

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        print('id:', task_id)
        task = Tasks.objects.filter(id=task_id).first()
        if task:
            task.completed = not task.completed  # Меняем статус
            task.save()
        # Перенаправляем на ту же страницу
        return redirect('tasks:task_list')

    context = {'tasks': tasks}

    return render(request, template_name, context)


def order_tasks(request, order_id):
    template_name = 'tasks/order_tasks.html'
    # Получаем задачи, связанные с указанным заказом
    tasks = Tasks.objects.values(
        'id',
        'worker__first_name',
        'worker__last_name',
        'worker__middle_name',
        'step',
        'description',
        'completed',
    ).filter(
        gold_order__order_id=order_id
    ).order_by('step')

    context = {'tasks': tasks, 'order_id': order_id}

    return render(request, template_name, context)


def add_task(request, order_id):
    template_name = 'tasks/add_task.html'

    order = get_object_or_404(GoldOrder, order_id=order_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.gold_order = order  # Привязываем задачу к заказу
            task.completed = False  # Поле по умолчанию
            task.save()
            return redirect('tasks:order_tasks', order_id=order_id)
    else:
        form = TaskForm()

    context = {'form': form, 'order': order}

    return render(request, template_name, context)


def edit_task(request, order_id, task_id):
    template_name = 'tasks/edit_task.html'
    order = get_object_or_404(GoldOrder, order_id=order_id)
    task = get_object_or_404(Tasks, id=task_id, gold_order=order)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:order_tasks', order_id=order_id)
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'order': order, 'task': task}

    return render(request, template_name, context)


def delete_task(request, order_id, task_id):
    template_name = 'tasks/delete_task.html'
    order = get_object_or_404(GoldOrder, order_id=order_id)
    task = get_object_or_404(Tasks, id=task_id, gold_order=order)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks:order_tasks', order_id=order_id)

    context = {'task': task, 'order': order}

    return render(request, template_name, context)
