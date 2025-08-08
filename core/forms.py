from django import forms
from .models import Student, Grade


class StudentForm(forms.ModelForm):
    """Form for adding and editing students"""
    
    class Meta:
        model = Student
        fields = ['full_name', 'father_phone_number', 'grade', 'is_exempt']
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
            }),
            'is_exempt': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            })
        }
        labels = {
            'full_name': 'الاسم الكامل',
            'father_phone_number': 'رقم هاتف الأب',
            'grade': 'الصف',
            'is_exempt': 'معفي من الحسابات'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required except is_exempt
        for field_name, field in self.fields.items():
            if field_name != 'is_exempt':
                field.required = True