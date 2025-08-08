from django.core.management.base import BaseCommand
from core.models import Grade, Student, Payment
import random


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating grades...')
        
        # Create grades
        grades_data = [
            ('grade7', 'الصف الأول الإعدادي'),
            ('grade8', 'الصف الثاني الإعدادي'),
            ('grade9', 'الصف الثالث الإعدادي'),
            ('grade10', 'الصف الأول الثانوي'),
            ('grade11', 'الصف الثاني الثانوي'),
            ('grade12', 'الصف الثالث الثانوي'),
        ]
        
        for grade_code, grade_name in grades_data:
            grade, created = Grade.objects.get_or_create(
                grade=grade_code,
                defaults={'monthly_fee': 500.00}
            )
            if created:
                self.stdout.write(f'Created grade: {grade_name}')

        self.stdout.write('Creating students...')
        
        # Sample student data
        students_data = [
            {
                'full_name': 'أحمد محمد علي',
                'grade': 'grade7',
                'father_phone_number': '01234567890',
            },
            {
                'full_name': 'فاطمة أحمد حسن',
                'grade': 'grade8',
                'father_phone_number': '01098765432',
            },
            {
                'full_name': 'محمد عبدالله سيد',
                'grade': 'grade9',
                'father_phone_number': '01123456789',
                
            },
            {
                'full_name': 'مريم حسام الدين',
                'grade': 'grade10',
                'father_phone_number': '01187654321',
                
            },
            {
                'full_name': 'يوسف خالد محمد',
                'grade': 'grade11',
                'father_phone_number': '01156789012',
            },
            {
                'full_name': 'نورا سامي أحمد',
                'grade': 'grade12',
                'father_phone_number': '01165432109',
            }
        ]
        
        for student_data in students_data:
            grade = Grade.objects.get(grade=student_data['grade'])
            student, created = Student.objects.get_or_create(
                full_name=student_data['full_name'],
                defaults={
                    'grade': grade,
                    'father_phone_number': student_data['father_phone_number'],
                }
            )
            if created:
                self.stdout.write(f'Created student: {student.full_name}')
                
                # Create payment records for each month
                months = ['august', 'september', 'october', 'november', 'december', 
                         'january', 'february', 'march', 'april', 'may', 'june']
                
                for month in months:
                    # Randomly assign payment status (70% chance of being paid)
                    is_paid = random.choice([True] * 7 + [False] * 3)
                    
                    Payment.objects.create(
                        student=student,
                        month=month,
                        year=2025,
                        amount=grade.monthly_fee,
                        is_paid=is_paid
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )