
from django.contrib import admin
from django.urls import path,include
from core.views import home
from django.conf import settings
from django.conf.urls.static import static
from tasks.views import TaskListView
urlpatterns = [
    path('',home,name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('tasks/<slug>/', TaskListView.as_view(), name='task_list'),
    path('tasks/filter/<slug:category_slug>/',home,name="category_wise_post"),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)