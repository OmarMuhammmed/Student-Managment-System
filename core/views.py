from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum, Q
from django.contrib import messages
from .models import Student, Grade, Payment
from .forms import StudentForm
import json
import csv


def dashboard(request):
    """Dashboard view with statistics"""
    # Get filter parameters
    selected_grades = request.GET.getlist('grades', [])
    
    # Base queryset
    students_qs = Student.objects.all()
    if selected_grades and 'all' not in selected_grades:
        students_qs = students_qs.filter(grade__grade__in=selected_grades)
    
    # Statistics
    total_students = students_qs.count()
    total_paid = Payment.objects.filter(
        student__in=students_qs, is_paid=True
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_pending = Payment.objects.filter(
        student__in=students_qs, is_paid=False
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Grade statistics
    grade_stats = students_qs.values(
        'grade__grade'
    ).annotate(
        student_count=Count('id')
    ).order_by('grade__grade')
    
    # All grades for filter
    all_grades = Grade.objects.all()
    
    context = {
        'total_students': total_students,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_grades': all_grades.count(),
        'grade_stats': grade_stats,
        'all_grades': all_grades,
        'selected_grades': selected_grades,
    }
    
    return render(request, 'core/dashboard.html', context)


def get_dashboard_stats(request):
    """AJAX endpoint to get updated dashboard statistics"""
    selected_grades = request.GET.getlist('grades', [])
    
    # Base queryset
    students_qs = Student.objects.all()
    if selected_grades and 'all' not in selected_grades:
        students_qs = students_qs.filter(grade__grade__in=selected_grades)
    
    # Statistics
    total_students = students_qs.count()
    total_paid = Payment.objects.filter(
        student__in=students_qs, is_paid=True
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_pending = Payment.objects.filter(
        student__in=students_qs, is_paid=False
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    return JsonResponse({
        'success': True,
        'data': {
            'total_students': total_students,
            'total_paid': float(total_paid),
            'total_pending': float(total_pending),
        }
    })


def grade_selection(request):
    """Grade selection view - required before accessing student list"""
    all_grades = Grade.objects.all().order_by('grade')
    
    context = {
        'all_grades': all_grades,
    }
    
    return render(request, 'core/grade_selection.html', context)


def students_list(request):
    """Students list view with payment tracking - requires grade selection"""
    # Get filter parameters
    selected_grades = request.GET.getlist('grades', [])
    
    # Require grade selection - redirect if no grades selected
    if not selected_grades or (len(selected_grades) == 1 and selected_grades[0] == ''):
        return render(request, 'core/grade_selection.html', {
            'all_grades': Grade.objects.all().order_by('grade'),
            'error_message': 'يرجى اختيار صف واحد على الأقل لعرض قائمة الطلاب'
        })
    
    # Base queryset
    students_qs = Student.objects.select_related('grade').prefetch_related('payments')
    if selected_grades and 'all' not in selected_grades:
        students_qs = students_qs.filter(grade__grade__in=selected_grades)
    
    # Check if any students exist for selected grades
    if not students_qs.exists():
        return render(request, 'core/grade_selection.html', {
            'all_grades': Grade.objects.all().order_by('grade'),
            'error_message': f'لا يوجد طلاب في الصفوف المحددة',
            'selected_grades': selected_grades
        })
    
    # Get all students with their payment data
    students_data = []
    months = ['august', 'september', 'october', 'november', 'december', 
              'january', 'february', 'march', 'april', 'may', 'june']
    
    # Initialize totals
    total_paid_amount = 0
    total_pending_amount = 0
    
    for student in students_qs:
        # Get payment status for each month
        payments = {}
        student_paid = 0
        student_pending = 0
        
        for month in months:
            payment = student.payments.filter(month=month, year=2025).first()
            if payment:
                payments[month] = payment.is_paid
                if payment.is_paid:
                    student_paid += float(payment.amount)
                    total_paid_amount += float(payment.amount)
                else:
                    student_pending += float(payment.amount)
                    total_pending_amount += float(payment.amount)
            else:
                payments[month] = False
                # Create pending payment record for calculation
                amount = float(student.grade.monthly_fee)
                student_pending += amount
                total_pending_amount += amount
        
        students_data.append({
            'student': student,
            'payments': payments,
            'total_paid': student_paid,
            'pending_amount': student_pending,
        })
    
    # All grades for filter
    all_grades = Grade.objects.all()
    
    # Get selected grade names for display
    selected_grade_names = []
    if 'all' in selected_grades:
        selected_grade_names = ['جميع الصفوف']
    else:
        for grade in all_grades:
            if grade.grade in selected_grades:
                selected_grade_names.append(grade.grade_name)
    
    context = {
        'students_data': students_data,
        'months': months,
        'all_grades': all_grades,
        'selected_grades': selected_grades,
        'selected_grade_names': selected_grade_names,
        'total_paid_amount': total_paid_amount,
        'total_pending_amount': total_pending_amount,
    }
    
    return render(request, 'core/students_list.html', context)


def student_detail(request, student_id):
    """Student detail view"""
    student = get_object_or_404(Student, id=student_id)
    
    # Get all payments for this student
    payments = student.payments.filter(year=2025).order_by('month')
    
    # Calculate statistics
    total_paid = payments.filter(is_paid=True).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_pending = payments.filter(is_paid=False).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    context = {
        'student': student,
        'payments': payments,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'completion_percentage': student.payment_completion_percentage,
    }
    
    return render(request, 'core/student_detail.html', context)


@csrf_exempt
def update_payment(request):
    """AJAX endpoint to update payment status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            month = data.get('month')
            is_paid = data.get('is_paid', False)
            
            student = get_object_or_404(Student, id=student_id)
            
            # Get or create payment record
            payment, created = Payment.objects.get_or_create(
                student=student,
                month=month,
                year=2025,
                defaults={
                    'amount': student.grade.monthly_fee,
                    'is_paid': is_paid
                }
            )
            
            if not created:
                payment.is_paid = is_paid
                payment.save()
            
            # Calculate updated totals for this student
            student_payments = student.payments.filter(year=2025)
            student_total_paid = student_payments.filter(is_paid=True).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            return JsonResponse({
                'success': True,
                'message': 'تم تحديث حالة الدفع بنجاح',
                'payment_amount': float(payment.amount),
                'student_total_paid': float(student_total_paid),
                'student_name': student.full_name
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'حدث خطأ: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'طريقة غير مسموحة'})


def monthly_revenue(request):
    """AJAX endpoint to get monthly revenue data"""
    month = request.GET.get('month', 'april')
    selected_grades = request.GET.getlist('grades', [])
    
    # Base queryset
    payments_qs = Payment.objects.filter(month=month, year=2025, is_paid=True)
    if selected_grades and 'all' not in selected_grades:
        payments_qs = payments_qs.filter(student__grade__grade__in=selected_grades)
    
    # Revenue by grade
    revenue_data = payments_qs.values(
        'student__grade__grade'
    ).annotate(
        total_revenue=Sum('amount'),
        student_count=Count('student', distinct=True)
    ).order_by('student__grade__grade')
    
    # Format data for frontend
    formatted_data = {}
    for item in revenue_data:
        grade = item['student__grade__grade']
        formatted_data[grade] = {
            'revenue': float(item['total_revenue']),
            'student_count': item['student_count']
        }
    
    return JsonResponse({
        'success': True,
        'data': formatted_data
    })


def export_students_csv(request):
    """Export students data to CSV"""
    import csv
    from django.http import HttpResponse
    
    selected_grades = request.GET.getlist('grades', [])
    
    # Base queryset
    students_qs = Student.objects.select_related('grade').prefetch_related('payments')
    if selected_grades and 'all' not in selected_grades:
        students_qs = students_qs.filter(grade__grade__in=selected_grades)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="students_data.csv"'
    
    # Add BOM for proper Arabic display in Excel
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Headers
    headers = ['الاسم', 'الصف', 'العمر', 'الهاتف', 'العنوان', 'إجمالي المدفوعات']
    months = ['أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر', 
              'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو']
    headers.extend(months)
    writer.writerow(headers)
    
    # Data rows
    month_keys = ['august', 'september', 'october', 'november', 'december', 
                  'january', 'february', 'march', 'april', 'may', 'june']
    
    for student in students_qs:
        row = [
            student.full_name,
            student.grade.grade_name,
            student.father_phone_number,
            student.total_payments
        ]
        
        # Add payment status for each month
        for month_key in month_keys:
            payment = student.payments.filter(month=month_key, year=2025).first()
            status = 'مدفوع' if payment and payment.is_paid else 'غير مدفوع'
            row.append(status)
        
        writer.writerow(row)
    
    return response


def add_student(request):
    """Add new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            
            # Create payment records for all months
            months = ['august', 'september', 'october', 'november', 'december', 
                     'january', 'february', 'march', 'april', 'may', 'june']
            
            for month in months:
                Payment.objects.create(
                    student=student,
                    month=month,
                    year=2025,
                    amount=student.grade.monthly_fee,
                    is_paid=False
                )
            
            messages.success(request, f'تم إضافة الطالب {student.full_name} بنجاح')
            return redirect('core:students_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = StudentForm()
    
    return render(request, 'core/add_student.html', {
        'form': form,
        'title': 'إضافة طالب جديد'
    })


def update_student(request, student_id):
    """Update student information"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث بيانات الطالب {student.full_name} بنجاح')
            return redirect('core:students_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'core/update_student.html', {
        'form': form,
        'student': student,
        'title': f'تعديل بيانات الطالب: {student.full_name}'
    })


def delete_student(request, student_id):
    """Delete student and all related payments"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()  # Payments will be deleted automatically due to CASCADE
        messages.success(request, f'تم حذف الطالب {student_name} بنجاح')
        return redirect('core:students_list')
    
    return render(request, 'core/delete_student.html', {
        'student': student,
        'title': f'حذف الطالب: {student.full_name}'
    })