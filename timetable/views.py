from django.shortcuts import render, redirect
from datetime import time, timedelta, datetime

from .models import Course, CourseSchedule
from .forms import CourseForm

def addCourse(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            generate_timetable()  # Generate timetable after adding course
            return redirect('timetable')  # Redirect to the timetable view
    else:
        form = CourseForm()

    context = {'form': form}
    return render(request, 'add_course.html', context)


def generate_timetable():
    classes = ['Class A', 'Class B', 'Class C', 'Class D', 'Class E', 'Class F']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    start_time = time(8, 0)  # 8 am
    end_time = time(14, 10)  # 2:10 pm
    period_duration = 40  # Duration in minutes

    timetable = []

    from datetime import datetime, time, timedelta

# ...

def generate_timetable():
    classes = ['Class A', 'Class B', 'Class C', 'Class D', 'Class E', 'Class F']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    start_time = time(8, 0)  # 8 am
    end_time = time(14, 10)  # 2:10 pm
    period_duration = 40  # Duration in minutes

    timetable = []

    for _class in classes:
        for day in days:
            current_time = datetime.combine(datetime.today(), start_time)  # Convert current_time to datetime
            while current_time.time() <= end_time:
                if day in ['Monday', 'Tuesday', 'Wednesday']:
                    period = CourseSchedule(class_name=_class, day=day, start_time=current_time.time(), end_time=(current_time + timedelta(minutes=period_duration)).time())
                    timetable.append(period)
                    current_time += timedelta(minutes=period_duration)
                else:
                    period = CourseSchedule(class_name=_class, day=day, start_time=current_time.time(), end_time=(current_time + timedelta(minutes=period_duration*2)).time())
                    timetable.append(period)
                    current_time += timedelta(minutes=period_duration*2)


    CourseSchedule.objects.all().delete()  # Clear existing schedule
    CourseSchedule.objects.bulk_create(timetable)  # Bulk create the new schedule

    morning_start_time = time(8, 0)  # 8 am
    morning_end_time = time(11, 0)  # 11 am
    double_period_courses = ['English', 'Maths', 'Programming']
    min_periods_per_week = 2

    current_time = start_time
    while current_time < end_time:
        if current_time.time() < morning_start_time or current_time.time() >= morning_end_time:
            # Afternoon slots
            for course in Course.objects.all():
                if course.duration == period_duration and course.name in double_period_courses:
                    CourseSchedule.objects.create(course=course, start_time=current_time, end_time=current_time + timedelta(minutes=80))
                else:
                    CourseSchedule.objects.create(course=course, start_time=current_time, end_time=current_time + timedelta(minutes=40))
            current_time += timedelta(minutes=period_duration)
        else:
            # Morning slots
            for course in Course.objects.filter(name__in=double_period_courses):
                CourseSchedule.objects.create(course=course, start_time=current_time, end_time=current_time + timedelta(minutes=80))
            current_time += timedelta(minutes=80)

    # Schedule remaining courses to meet the requirement of 2 periods per week
    for course in Course.objects.all():
        if CourseSchedule.objects.filter(course=course).count() < min_periods_per_week:
            # Schedule additional slot for the course to meet the requirement
            pass

    return True
