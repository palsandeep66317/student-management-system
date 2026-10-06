from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance


@login_required(login_url='login')
def dashboard(request):
    students = Student.objects.count()
    total_attendance = Attendance.objects.count()
    present = Attendance.objects.filter(status='Present').count()
    absent = Attendance.objects.filter(status='Absent').count()

    recent_students = Student.objects.all().order_by('-id')[:5]

    recent_attendance = Attendance.objects.select_related(
        'student'
    ).order_by('-date', '-id')[:5]

    return render(request, 'students/dashboard.html', {
        'students': students,
        'total_attendance': total_attendance,
        'present': present,
        'absent': absent,
        'recent_students': recent_students,
        'recent_attendance': recent_attendance,
    })


@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        course = request.POST.get('course', '').strip()
        semester = request.POST.get('semester', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([
            student_id, name, email, phone,
            course, semester, date_of_birth, address
        ]):
            return render(request, 'students/add_student.html', {
                'error': 'Please fill all fields.'
            })

        if Student.objects.filter(student_id=student_id).exists():
            return render(request, 'students/add_student.html', {
                'error': 'Student ID already exists.'
            })

        if Student.objects.filter(email=email).exists():
            return render(request, 'students/add_student.html', {
                'error': 'Email already exists.'
            })

        Student.objects.create(
            student_id=student_id,
            name=name,
            email=email,
            phone=phone,
            course=course,
            semester=semester,
            date_of_birth=date_of_birth,
            address=address
        )

        messages.success(request, 'Student added successfully!')
        return redirect('student_list')

    return render(request, 'students/add_student.html')


@login_required(login_url='login')
def student_list(request):
    query = request.GET.get('q', '')

    if query:
        students = Student.objects.filter(
            name__icontains=query
        ) | Student.objects.filter(
            student_id__icontains=query
        ) | Student.objects.filter(
            email__icontains=query
        ) | Student.objects.filter(
            course__icontains=query
        )
    else:
        students = Student.objects.all()

    return render(request, 'students/student_list.html', {
        'students': students,
        'query': query
    })


@login_required(login_url='login')
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    attendance_records = Attendance.objects.filter(student=student)

    total_classes = attendance_records.count()
    present = attendance_records.filter(status='Present').count()
    absent = attendance_records.filter(status='Absent').count()

    if total_classes > 0:
        attendance_percentage = round(
            (present / total_classes) * 100,
            2
        )
    else:
        attendance_percentage = 0

    return render(request, 'students/student_detail.html', {
        'student': student,
        'total_classes': total_classes,
        'present': present,
        'absent': absent,
        'attendance_percentage': attendance_percentage,
    })


@login_required(login_url='login')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        course = request.POST.get('course', '').strip()
        semester = request.POST.get('semester', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([
            student_id, name, email, phone,
            course, semester, date_of_birth, address
        ]):
            return render(request, 'students/edit_student.html', {
                'student': student,
                'error': 'Please fill all fields.'
            })

        if Student.objects.filter(
            student_id=student_id
        ).exclude(id=student.id).exists():
            return render(request, 'students/edit_student.html', {
                'student': student,
                'error': 'Student ID already exists.'
            })

        if Student.objects.filter(
            email=email
        ).exclude(id=student.id).exists():
            return render(request, 'students/edit_student.html', {
                'student': student,
                'error': 'Email already exists.'
            })

        student.student_id = student_id
        student.name = name
        student.email = email
        student.phone = phone
        student.course = course
        student.semester = semester
        student.date_of_birth = date_of_birth
        student.address = address

        student.save()

        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')

    return render(request, 'students/edit_student.html', {
        'student': student
    })


@login_required(login_url='login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')

    return redirect('student_list')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'students/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'students/login.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_attendance(request):
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('date')
        status = request.POST.get('status')

        student = get_object_or_404(
            Student,
            id=student_id
        )

        Attendance.objects.create(
            student=student,
            date=date,
            status=status
        )

        messages.success(request, 'Attendance added successfully!')
        return redirect('attendance_list')

    return render(request, 'students/add_attendance.html', {
        'students': students
    })


@login_required(login_url='login')
def attendance_list(request):
    attendance = Attendance.objects.select_related(
        'student'
    ).all().order_by('-date')

    return render(request, 'students/attendance_list.html', {
        'attendance': attendance
    })


@login_required(login_url='login')
def edit_attendance(request, id):
    attendance = get_object_or_404(
        Attendance,
        id=id
    )

    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('date')
        status = request.POST.get('status')

        attendance.student = get_object_or_404(
            Student,
            id=student_id
        )

        attendance.date = date
        attendance.status = status
        attendance.save()

        messages.success(request, 'Attendance updated successfully!')
        return redirect('attendance_list')

    return render(request, 'students/edit_attendance.html', {
        'attendance': attendance,
        'students': students
    })


@login_required(login_url='login')
def delete_attendance(request, id):
    attendance = get_object_or_404(
        Attendance,
        id=id
    )

    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance deleted successfully!')

    return redirect('attendance_list')


@login_required(login_url='login')
def attendance_report(request, id):
    student = get_object_or_404(
        Student,
        id=id
    )

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total_classes = attendance_records.count()

    present = attendance_records.filter(
        status='Present'
    ).count()

    absent = attendance_records.filter(
        status='Absent'
    ).count()

    if total_classes > 0:
        attendance_percentage = round(
            (present / total_classes) * 100,
            2
        )
    else:
        attendance_percentage = 0

    return render(
        request,
        'students/attendance_report.html',
        {
            'student': student,
            'attendance_records': attendance_records,
            'total_classes': total_classes,
            'present': present,
            'absent': absent,
            'attendance_percentage': attendance_percentage,
        }
    )