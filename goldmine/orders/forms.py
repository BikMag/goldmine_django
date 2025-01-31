from django import forms
from django.utils.timezone import now
from .models import GoldOrder, OrderStates, Employee


class OrderStatusAndManagerForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=OrderStates.objects.all(),
        empty_label="Выберите статус",
        label="Статус заказа",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    manager = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__name='Менеджер'),
        empty_label="Выберите менеджера",
        label="Менеджер",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = GoldOrder
        fields = ['gold_amount', 'deadline']
        labels = {
            'gold_amount': 'Количество золота (т)',
            'deadline': 'Дата сдачи заказа',
        }
        widgets = {
            'gold_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'step': 0.1}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline <= now().date():  # Сравниваем только даты (без времени)
            raise forms.ValidationError(
                "Дата сдачи заказа должна быть позже текущей даты.")
        return deadline
