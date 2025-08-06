from django.db import models


class Grade(models.Model):
    GRAD_NAMES = [
        ('grade1','الصف الأول الإعدادي'),
        ('grade2','الصف الثاني الإعدادي'),
        ('grade3','الصف الثالث الإعدادي'),  
        ('grade4','الصف الأول الثانوي'),
        ('grade5','الصف الثاني الثانوي'),     
        ('grade6','الصف الثالث الثانوي'),
    ]
    grade = models.CharField(
        max_length=10,           
        choices=GRAD_NAMES,
    )

    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
   

    def __str__(self):
        return self.grade

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    father_phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']


class Payment(models.Model):
    MONTH_CHOICES = [
        (8, 'أغسطس'), (9, 'سبتمبر'), (10, 'أكتوبر'), (11, 'نوفمبر'),
        (12, 'ديسمبر'), (1, 'يناير'), (2, 'فبراير'), (3, 'مارس'),
        (4, 'أبريل'), (5, 'مايو'), (6, 'يونيو'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)       

    class Meta:
        unique_together = ('student', 'month', 'year')

    def __str__(self):
        return f"{self.student.full_name} - {self.get_month_display()} {self.year}"