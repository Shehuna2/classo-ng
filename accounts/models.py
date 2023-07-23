from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



ROLES = (
    ('ADMINISTRATION', 'ADMINISTRATION'),
    ('TEACHING STAFF', 'TEACHING STAFF'),
    ('VISITOR', 'VISITOR'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)  # Add the 'name' field
    role = models.CharField(max_length=14, choices=ROLES)

    def __str__(self):
        return f"{self.user.username}"
    

class RecentPdfDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_downloads')
    pdf_file = models.FileField(upload_to='pdf_downloads/')
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pdf_file.name}"



