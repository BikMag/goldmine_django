from django.db import models
from orders.models import Employee, GoldOrder


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    gold_order = models.ForeignKey(
        GoldOrder, models.DO_NOTHING, db_column='gold_order',
        verbose_name='Заказ'
    )
    worker = models.ForeignKey(
        Employee, models.DO_NOTHING, db_column='worker',
        verbose_name='Рабочий'
    )
    description = models.TextField(verbose_name='Задача')
    completed = models.BooleanField(verbose_name='Выполнен')
    step = models.IntegerField(verbose_name='Шаг')

    class Meta:
        managed = False
        db_table = 'tasks'
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def __str__(self):
        return f'{self.gold_order} для {self.worker} - {self.description}'
