# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete`
#        set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create,
#       modify, and delete the table
# Feel free to rename the models, but don't rename db_table values
#       or field names.
from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    middle_name = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Отчество')
    organization = models.CharField(max_length=30, verbose_name='Организация')
    phone_number = models.CharField(
        unique=True, max_length=20, verbose_name='Номер телефона')
    email = models.CharField(unique=True, max_length=30,
                             blank=True, null=True, verbose_name='Эл. почта')

    class Meta:
        managed = False
        db_table = 'customer'
        verbose_name = 'заказчик'
        verbose_name_plural = 'заказчики'

    def __str__(self):
        if self.middle_name is None:
            return f'{self.last_name} {self.first_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    middle_name = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Отчество')
    phone_number = models.CharField(
        unique=True, max_length=20, verbose_name='Номер телефона')
    position = models.ForeignKey(
        'Position', models.DO_NOTHING, verbose_name='Звание')

    class Meta:
        managed = False
        db_table = 'employee'
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

        ordering = ('last_name', 'first_name', 'middle_name',)

    def __str__(self):
        if self.middle_name is None:
            return f'{self.last_name} {self.first_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'


class GoldOrder(models.Model):
    order_id = models.AutoField(primary_key=True, verbose_name='№ заказа')
    customer = models.ForeignKey(
        Customer, models.DO_NOTHING, verbose_name='Заказчик')
    employee = models.ForeignKey(
        Employee, models.DO_NOTHING, verbose_name='Менеджер')
    gold_amount = models.IntegerField(verbose_name='Количество золота')
    ordering_date = models.DateField(verbose_name='Срок оформления заказа')
    deadline = models.DateField(verbose_name='Срок сдачи заказа')
    status = models.ForeignKey(
        'OrderStates',
        models.RESTRICT,
        db_column='status',
        blank=True,
        null=True,
        verbose_name='Статус заказа'
    )

    class Meta:
        managed = False
        db_table = 'gold_order'
        unique_together = (('order_id', 'customer', 'employee'),)
        ordering = ('-ordering_date',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ №{self.order_id} от {self.ordering_date}'


class OrderStates(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=20,
                            verbose_name='Название')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'order_states'
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'

    def __str__(self):
        return self.name


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='Звание')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'position'
        verbose_name = 'звание'
        verbose_name_plural = 'звания'

    def __str__(self):
        return self.name


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey(
# 'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'
