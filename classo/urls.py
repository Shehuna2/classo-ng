from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', include('core.urls')),
]

# 1258240058397116
# d4bd00a1f80a16f16bed46d8b5f780a4
