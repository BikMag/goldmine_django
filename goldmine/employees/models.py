from django.db import models


class EmployeesView(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_full_name = models.CharField(max_length=30, verbose_name='ФИО')
    phone_number = models.CharField(
        unique=True, max_length=20, verbose_name='Номер телефона')
    position_name = models.CharField(max_length=20, verbose_name='Звание')
    position_description = models.TextField(
        blank=True, null=True, verbose_name='Описание звания')

    class Meta:
        managed = False
        db_table = 'view_employee_position'
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

        ordering = ('employee_full_name',)
