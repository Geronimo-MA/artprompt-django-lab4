from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Панель управления ArtPrompt'
admin.site.site_title = 'ArtPrompt Администрирование'
admin.site.index_title = 'Управление арт-промптами и художественными идеями'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('artprompt.urls')),
]