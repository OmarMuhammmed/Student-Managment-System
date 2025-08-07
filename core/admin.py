from django.contrib import admin
from .models import Grade, Student, Payment


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade', 'grade_name', 'monthly_fee']
    list_editable = ['monthly_fee']
    ordering = ['grade']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'grade', 'father_phone_number']
    list_filter = ['grade']
    search_fields = ['full_name', 'father_phone_number']
    ordering = ['full_name']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('full_name', 'grade')
        }),
        ('معلومات الاتصال', {
            'fields': ('father_phone_number',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'month', 'year', 'amount', 'is_paid', 'paid_at']
    list_filter = ['month', 'year', 'is_paid', 'student__grade']
    search_fields = ['student__full_name']
    list_editable = ['is_paid']
    ordering = ['-year', 'month', 'student__full_name']
    
    fieldsets = (
        ('معلومات الدفع', {
            'fields': ('student', 'month', 'year', 'amount')
        }),
        ('حالة الدفع', {
            'fields': ('is_paid', 'paid_at')
        }),
    )
    
    readonly_fields = ['paid_at']


# Customize admin site
admin.site.site_header = "نظام إدارة الطلاب - الأستاذ محمد علي"
admin.site.site_title = "إدارة الطلاب"
admin.site.index_title = "لوحة التحكم"