from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.contrib.auth import get_user_model




STATUS = (
    ('draft', 'draft'),
    ('published', 'published'),
)

TERMS = (
    ('1st', '1st Term'),
    ('2nd', '2nd Term'),
    ('3rd', '3rd Term'),
    ('summer', 'Summer Courses'),
    
)

class Section(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topic_course')
    name = models.CharField(max_length=200)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='topics')
    terms = models.CharField(max_length=13, choices=TERMS, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    weeks = models.IntegerField(default=0)
    l_note = RichTextUploadingField()
    l_plan = RichTextUploadingField()
    tests = RichTextUploadingField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        self.id

class Exam(models.Model):
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_exam')
    term = models.CharField(max_length=13, choices=TERMS, blank=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='exam')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self) -> str:
        return f"{self.subject} - {self.term}"
    
    def get_absolute_url(self):
        return reverse('core:exam-details', args=[str(self.id)])
    
class Curriculum(models.Model):
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriclulum')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='class_cur')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self) -> str:
        return f"{self.subject} - {self.classroom}"
    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}"

class Download(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, null=True, default=None)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    curriculum = models.ForeignKey('Curriculum', on_delete=models.CASCADE, null=True, default=None)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.subject}"
