from django.db import models


class Student(models.Model):
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
        ]

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
        ordering = ["-posted_date"]
        indexes = [
            models.Index(fields=["title"], name="title_idx"),
        ]


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')

    def __str__(self):
        return f"Application of {self.student} for {self.vacancy}"
    
    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ["-application_date"]
        indexes = [
            models.Index(fields=["status"], name="status_idx"),
        ]
