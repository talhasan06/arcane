
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from core.views import product,contact,about_us
from .views import TaskCreateView,CompletedTaskListView,RemainingTaskListView,TaskDetailView,create_category,ToggleCompleteView,delete_task,remove_task,EditTaskView
urlpatterns = [
    path('products/',product,name='product'),
    path('contact/',contact,name='contact'),
    path('about/',about_us,name='about'),
    path('add_task/',TaskCreateView.as_view(),name='add_task'),
    path('add_category/',create_category,name='add_category'),
    path('completed/',CompletedTaskListView.as_view(), name='completed'),
    path('remaining/',RemainingTaskListView.as_view(), name='remaining'),
    path('toggle_complete/<int:task_id>/',ToggleCompleteView.as_view(), name='toggle_complete'),
    path('detail/<int:task_id>/',TaskDetailView.as_view(), name='task_detail'),
    path('delete/<int:task_id>/',delete_task, name='delete'),
    path('remove_task/<int:task_id>/',remove_task, name='remove_task'),
    path('edit_task/<int:task_id>/', EditTaskView.as_view(), name='edit_task'),
]