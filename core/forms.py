from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title', 'required': 'required'}),
            'priority': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_completed', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # enforce server-side required flags as well
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['due_date'].required = True
        self.fields['priority'].required = True
        # Make completed required as well (user must explicitly mark completion)
        self.fields['completed'].required = True

    def clean_due_date(self):
        data = self.cleaned_data.get('due_date')
        if data:
            from django.utils import timezone
            if data < timezone.localdate():
                raise forms.ValidationError('Due date cannot be in the past.')
        return data


class QuickTaskForm(forms.ModelForm):
    """A smaller form used on the dashboard quick-create widget.

    Only includes fields necessary for a quick task: title, description and due_date.
    Priority and completed use the model defaults when saving.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
        }

    def clean_due_date(self):
        data = self.cleaned_data.get('due_date')
        if data:
            from django.utils import timezone
            if data < timezone.localdate():
                raise forms.ValidationError('Due date cannot be in the past.')
        return data