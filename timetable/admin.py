from django.contrib import admin

from .models import Course, CourseSchedule

admin.site.register(Course)
admin.site.register(CourseSchedule)