from django.contrib import admin
from django.urls import path
from students import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Add Student
    path('add-student/', views.add_student, name='add_student'),

    # Student List
    path('students/', views.student_list, name='student_list'),

    # Edit Student
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),

    # Delete Student
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('login/', views.user_login, name='login'),

path('logout/', views.user_logout, name='logout'),
path('student/<int:id>/', views.student_detail, name='student_detail'),
path('attendance/add/', views.add_attendance, name='add_attendance'),

path('attendance/', views.attendance_list, name='attendance_list'),
path(
    'attendance/edit/<int:id>/',
    views.edit_attendance,
    name='edit_attendance'
),

path(
    'attendance/delete/<int:id>/',
    views.delete_attendance,
    name='delete_attendance'
),
path(
    'student/<int:id>/attendance/',
    views.attendance_report,
    name='attendance_report'
),
]