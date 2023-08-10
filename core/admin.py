from django.contrib import admin

from .models import Section, Classroom, Course, Topic, Exam, Curriculum, Contact, Download

@admin.register(Exam)
class ExamsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'term', 'classroom', 'status')
    list_filter = ('status', 'classroom', 'term')
    search_fields =('subject', 'term', 'classroom')

@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'terms', 'classroom', 'weeks', 'name', 'status')
    list_filter = ('status', 'name', 'classroom')
    search_fields =('subject', 'name', 'classroom')


admin.site.register(Section)
admin.site.register(Classroom)
admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Contact)
admin.site.register(Download)
