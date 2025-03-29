from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    

class University(models.Model):
    name=models.CharField(max_length=50)
    campus=models.CharField(max_length=50)
    type=models.CharField(max_length=50, choices=[('Public', 'Public'), ('Private', 'Private')])
    university_logo=models.ImageField(upload_to='university_logos/', blank=True, null=True)
    main_website_link=models.URLField()
    main_email=models.EmailField()
    main_phone_number=models.TextField()
    

    def  __str__(self):
        return self.name
 

class Program(models.Model):
    university=models.ForeignKey(University, on_delete=models.CASCADE, related_name="programs")
    name=models.CharField(max_length=100)
  
    
   
    def __str__(self):
        return f"{self.name}-{self.university.name}"
    

class ProgramType(models.Model):
    program=models.ForeignKey(Program, on_delete=models.CASCADE, related_name="program_types")
    university=models.ForeignKey(University, on_delete=models.CASCADE, related_name='program_types', null=True, blank=True )
    PROGRAM_TYPES=[
        ("degree","Bachelor's Degree"),
        ("diploma","Diploma"),
        ("certificate","Certificate")
    ]
    type=models.CharField(max_length=100, choices=PROGRAM_TYPES)
    entry_requirements=models.TextField()
    duration=models.CharField(max_length=50)
    department=models.TextField()
    phone_number=models.TextField()
    Email=models.EmailField()
    website_link=models.URLField()


    def __str__(self):
        return f"{self.program.name} - {self.get_type_display()}- {self.university.name}"
    

class SavedProgram(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'program')  # Ensures a user can only save a program once

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"
