from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    semester = models.IntegerField()
    date_of_birth = models.DateField()
    address = models.TextField()
    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance'
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent'),
        ]
    )

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"