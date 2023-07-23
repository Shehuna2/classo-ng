from .models import Section, Course, Classroom, Topic, Exam

def section_list(request):
    sections = Section.objects.all()
    return {'sections':sections}

def topic_list(request):
    topics = Topic.objects.all() 
    return {'topics':topics}

def exam_list(request):
    exams = Exam.objects.all() 
    return {'exams':exams}