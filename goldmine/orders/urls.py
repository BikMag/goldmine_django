from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.create_order, name='create_order'),
    path('<int:pk>/', views.order_info, name='order_info'),
    path('<int:pk>/change-status/', views.manager_change_order,
         name='manager_change_order'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    path('<int:pk>/delete/', views.delete_order, name='delete_order'),
]
