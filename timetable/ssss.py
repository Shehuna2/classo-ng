# Assuming a CourseSchedule model to represent the timetable slots

from datetime import time

def generate_timetable():
    # Clear existing timetable slots
    CourseSchedule.objects.all().delete()

    # Define class timings
    start_time = time(8, 0)  # 8 am
    end_time = time(14, 10)  # 2:10 pm
    period_duration = 40  # Duration in minutes

    # Define course timings
    morning_start_time = time(8, 0)  # 8 am
    morning_end_time = time(11, 0)  # 11 am
    double_period_courses = ['English', 'Maths', 'Programming']
    min_periods_per_week = 2

    # Generate timetable slots
    current_time = start_time
    while current_time < end_time:
        if current_time.time() < morning_start_time or current_time.time() >= morning_end_time:
            # Afternoon slots
            for course in Course.objects.all():
                # Check if the course needs to be scheduled
                if course.duration == period_duration and course.name in double_period_courses:
                    # Add double period slot
                    CourseSchedule.objects.create(course=course, start_time=current_time, end_time=current_time + timedelta(minutes=80))
                else:
                    # Add single period slot
                    CourseSchedule.objects.create(course=course, start_time=current_time, end_time=current_time + timedelta(minutes=40))

            # Move to the next period
            current_time += timedelta(minutes=period_duration)
        else:
            # Morning slots
            for course in Course.objects.filter(name__in=double_period_courses):
                # Add double period slot
                CourseSchedule.objects.create(course=course, start_time=current_time, end_time=current_time + timedelta(minutes=80))

            # Move to the next period
            current_time += timedelta(minutes=80)

    # Schedule remaining courses to meet the minimum periods per week requirement
    for course in Course.objects.all():
        if CourseSchedule.objects.filter(course=course).count() < min_periods_per_week:
            # Schedule additional slots for the course to meet the requirement

    return True
