from django.contrib import admin
from .models import Grade, Student, Payment


admin.site.register(Student)
admin.site.register(Grade)
admin.site.register(Payment)