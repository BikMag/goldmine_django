from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('worker-tasks/', views.task_list, name='task_list'),
    path('order-tasks/<int:order_id>/', views.order_tasks, name='order_tasks'),
    path('order-tasks/<int:order_id>/add/', views.add_task, name='add_task'),
    path('order-tasks/<int:order_id>/edit/<int:task_id>/',
         views.edit_task, name='edit_task'),
    path('order-tasks/<int:order_id>/delete/<int:task_id>/',
         views.delete_task, name='delete_task'),
]
