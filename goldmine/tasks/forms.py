from django import forms
from .models import Employee, Tasks


class TaskForm(forms.ModelForm):
    worker = forms.ModelChoiceField(
        queryset=Employee.objects.exclude(position__name='Менеджер'),
        label="Рабочий",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    completed = forms.BooleanField(
        label="Выполнено",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Tasks
        fields = ['step', 'description', 'worker', 'completed']
        labels = {
            'step': 'Шаг задачи',
            'description': 'Описание задачи',
            'worker': 'Выберите рабочего',
            'completed': 'Статус выполнения',
        }
        widgets = {
            'step': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder':
                'Введите шаг задачи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':
                'Введите описание задачи'
            }),
        }
