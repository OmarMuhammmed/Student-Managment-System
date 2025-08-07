from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/select-grade/', views.grade_selection, name='grade_selection'),
    path('students/', views.students_list, name='students_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/update/', views.update_student, name='update_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('api/update-payment/', views.update_payment, name='update_payment'),
    path('api/monthly-revenue/', views.monthly_revenue, name='monthly_revenue'),
    path('api/dashboard-stats/', views.get_dashboard_stats, name='dashboard_stats'),
    path('export/students-csv/', views.export_students_csv, name='export_students_csv'),
]