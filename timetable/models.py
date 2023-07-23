from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=300)
    teacher = models.CharField(max_length=300)
    duration = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def get_course_name_for_day(self, day):
        # Implement this method to retrieve the course name for a specific day
        # You can use filters or conditions to get the course name based on the day
        return self.course.name