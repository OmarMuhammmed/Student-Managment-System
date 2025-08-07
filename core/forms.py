from django import forms
from .models import Student, Grade


class StudentForm(forms.ModelForm):
    """Form for adding and editing students"""
    
    class Meta:
        model = Student
        fields = ['full_name', 'father_phone_number', 'grade']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-3 py-2',
                'placeholder': 'أدخل الاسم الكامل'
            }),
            'father_phone_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-3 py-2',
                'placeholder': 'أدخل رقم هاتف الأب'
            }),
            'grade': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-3 py-2'
            })
        }
        labels = {
            'full_name': 'الاسم الكامل',
            'father_phone_number': 'رقم هاتف الأب',
            'grade': 'الصف'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required
        for field in self.fields.values():
            field.required = True