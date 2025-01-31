from django.contrib import admin
from .models import Customer, Employee, GoldOrder, OrderStates, Position
from tasks.models import Tasks


class GoldOrderInline(admin.TabularInline):
    model = GoldOrder
    extra = 0


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0


class TasksInline(admin.TabularInline):
    model = Tasks
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'organization',
        'phone_number',
        'email',
    )
    search_fields = ('phone_number',)
    inlines = (
        GoldOrderInline,
    )

    def full_name(self, obj):
        if obj.middle_name is None:
            return f'{obj.last_name} {obj.first_name[0]}.'
        return f'{obj.last_name} {obj.first_name[0]}.{obj.middle_name[0]}.'
    full_name.short_description = 'ФИО'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'position',
        'phone_number',
    )
    list_filter = ('position',)
    inlines = (
        GoldOrderInline,
        TasksInline,
    )

    def full_name(self, obj):
        if obj.middle_name is None:
            return f'{obj.last_name} {obj.first_name[0]}.'
        return f'{obj.last_name} {obj.first_name[0]}.{obj.middle_name[0]}.'
    full_name.short_description = 'ФИО'


class GoldOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'customer',
        'employee',
        'gold_amount',
        'ordering_date',
        'deadline',
        'status',
    )
    list_editable = (
        'status',
    )
    search_fields = ('order_id', 'gold_amount',)
    list_filter = ('status',)


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    inlines = (
        EmployeeInline,
    )


class TasksAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'step',
        'worker',
        'gold_order',
        'completed',
    )
    list_editable = (
        'completed',
    )


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(GoldOrder, GoldOrderAdmin)
admin.site.register(OrderStates)
admin.site.register(Position, PositionAdmin)
admin.site.register(Tasks, TasksAdmin)
