from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.template.loader import get_template
from random import choice, random, sample
from xhtml2pdf import pisa
from io import BytesIO

from .models import Topic, Exam, Curriculum, Download
from .forms import TopicForm, ExamForm, ContactForm

def addTopic(request):
    if request.method == 'POST':
        t_form = TopicForm(request.POST)
        if t_form.is_valid():
            t_form.save()
            return redirect('core:home')
            messages.success(request, "Congrtas, topic created succesafully!")
    else:
        messages.error(request, "Failed, check your submission and try again!")
        t_form = TopicForm()

    return render(request, 'add_topic.html', {'t_form':t_form, 'messages':messages})

def addExam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:exams-list')
    else:
        form = ExamForm()

    return render(request, 'add_exam.html', {'form':form})

def home(request, section_name=None):
    topics = Topic.objects.filter(status='published')
    exams = Exam.objects.filter(status='published')

    query = request.GET.get('q')
    if query:
        topics = topics.filter(
            Q(name__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(classroom__name__icontains=query) |
            Q(classroom__section__name__icontains=query)
        ).distinct()

    if section_name:
        section_topics = topics.filter(classroom__section__name=section_name)
    else:
        section_topics = topics

    section_topics = section_topics.order_by('id')

    # Pagination
    topics_per_page = 14 

    paginator = Paginator(section_topics, topics_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'topics': page,
        'exams': exams,
    }
    return render(request, 'topic_list.html', context)


def render_to_pdf(template_path, context_dict, request):
    template = get_template(template_path)
    html = template.render(context_dict, request)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def topicDetails(request, id):
    topic = get_object_or_404(Topic, id=id)
    
    context = {
        'topic':topic,
        'user': request.user,
    }
    if request.GET.get('format') == 'pdf':
        if request.user.is_authenticated:
            pdf = render_to_pdf('topic_details.html', context, request)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="topic_details.pdf"'
                return response
        else:
            return redirect('accounts:login')
    return render(request, 'topic_details.html', context)

# list total exams available
def examList(request, section_name=None):
    exams = Exam.objects.filter(status='published')

    query = request.GET.get('q')
    if query:
        exams = exams.filter(
            Q(subject__name__icontains=query) |
            Q(term__icontains =query) |
            Q(classroom__name__icontains=query) |
            Q(classroom__section__name__icontains=query)
        ).distinct()


    if section_name:
        section_exams = exams.filter(classroom__section__name=section_name)
    else:
        section_exams = exams

    section_exams = section_exams.order_by('id')

    exams_per_page = 14 

    paginator = Paginator(section_exams, exams_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'exams':page,
    }
    return render(request, 'exams.html', context)

 # Make sure to import the custom render_to_pdf function from your render.py

@login_required
def examDetails(request, id):
    exam = get_object_or_404(Exam, id=id)
    user = request.user

    context = {
        'exam': exam,
        'user': user,
    }

    if request.GET.get('format') == 'pdf':
        if user.is_authenticated:
            pdf = render_to_pdf('exam_details.html', context, request)  # Don't pass the request object
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="exam_details.pdf"'
                Download.objects.create(user=request.user, exam=exam)  # Create a new Download object
                return response
        else:
            return redirect('accounts:login')
                

    return render(request, 'exam_details.html', context)

def curriculumList(request, section_name=None):
    curriculums = Curriculum.objects.filter(status='published')

    query = request.GET.get('q')
    if query:
        curriculums = curriculums.filter(
            Q(subject__name__icontains=query) |
            Q(classroom__name__icontains=query) |
            Q(classroom__section__name__icontains=query)
        ).distinct()

    if section_name:
        section_curriculum = curriculums.filter(classroom__section__name=section_name)
    else:
        section_curriculum = curriculums

    section_curriculum = section_curriculum.order_by('id')

    # Pagination
    curriculums_per_page = 10 

    paginator = Paginator(section_curriculum, curriculums_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'curriculums': page,
    }
    return render(request, 'curriculum_list.html', context)

def curriculumDetails(request, id):
    curriculum = get_object_or_404(Curriculum, id=id)
    
    context = {
        'curriculum':curriculum, 
        'user': request.user,
    }
    if request.GET.get('format') == 'pdf':
        if request.user.is_authenticated:
            pdf = render_to_pdf('curriculum_details.html', context, request)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="curriculum_details.pdf"'
                return response
        else:
            return redirect('accounts:login')
    return render(request, 'curriculum_details.html', context)

def contactUs(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            form.save()
            return render(request, 'success.html')

    else:
        form = ContactForm()

    context = {'form':form}

    return render(request, 'contact.html', context)
