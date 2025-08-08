from django.db import models
from django.utils import timezone


class Grade(models.Model):
    GRADE_CHOICES = [
        ('grade7', 'الصف الأول الإعدادي'),
        ('grade8', 'الصف الثاني الإعدادي'),
        ('grade9', 'الصف الثالث الإعدادي'),  
        ('grade10', 'الصف الأول الثانوي'),
        ('grade11', 'الصف الثاني الثانوي'),     
        ('grade12', 'الصف الثالث الثانوي'),
    ]
    
    grade = models.CharField(
        max_length=10,           
        choices=GRADE_CHOICES,
        unique=True
    )
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    
    class Meta:
        ordering = ['grade']
   
    def __str__(self):
        return dict(self.GRADE_CHOICES)[self.grade]
    
    @property
    def grade_name(self):
        return dict(self.GRADE_CHOICES)[self.grade]

class Student(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="الصف")
    father_phone_number = models.CharField(max_length=20, verbose_name="رقم هاتف الأب")
    is_exempt = models.BooleanField(default=False, verbose_name="معفي من الحسابات")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"
    
    @property
    def total_payments(self):
        """Calculate total amount paid by student"""
        return self.payments.filter(is_paid=True).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    @property
    def pending_payments(self):
        """Calculate pending payment amount"""
        return self.payments.filter(is_paid=False).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    @property
    def payment_completion_percentage(self):
        """Calculate payment completion percentage"""
        total_months = 11  # August to June
        paid_months = self.payments.filter(is_paid=True, year=2025).count()
        return (paid_months / total_months) * 100 if total_months > 0 else 0
    
    @property
    def payment_completion_percentage(self):
        """Calculate payment completion percentage"""
        total_payments = self.payments.count()
        paid_payments = self.payments.filter(is_paid=True).count()
        if total_payments == 0:
            return 0
        return round((paid_payments / total_payments) * 100, 2)


class Payment(models.Model):
    MONTH_CHOICES = [
        ('august', 'أغسطس'), ('september', 'سبتمبر'), ('october', 'أكتوبر'), 
        ('november', 'نوفمبر'), ('december', 'ديسمبر'), ('january', 'يناير'), 
        ('february', 'فبراير'), ('march', 'مارس'), ('april', 'أبريل'), 
        ('may', 'مايو'), ('june', 'يونيو'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    month = models.CharField(max_length=10, choices=MONTH_CHOICES, verbose_name="الشهر")
    year = models.IntegerField(default=2025, verbose_name="السنة")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ")
    is_paid = models.BooleanField(default=False, verbose_name="مدفوع")
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name="تاريخ الدفع")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'month', 'year')
        ordering = ['year', 'month']
        verbose_name = "دفعة"
        verbose_name_plural = "الدفعات"

    def __str__(self):
        return f"{self.student.full_name} - {self.get_month_display()} {self.year}"
    
    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.student.grade.monthly_fee
        if self.is_paid and not self.paid_at:
            self.paid_at = timezone.now()
        elif not self.is_paid:
            self.paid_at = None
        super().save(*args, **kwargs)