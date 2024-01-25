
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,DetailView
from .models import Task,Category
from .forms import TaskForm,CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

categories = Category.objects.all()

class TaskListView(View):
    def get_template_name(self, slug):
        template_mapping = {
            'due-date': 'sort_templates/task_list_due_date.html',
            'priority': 'sort_templates/task_list_priority.html',
            'category': 'sort_templates/task_list_category.html',
        }

        default_template = 'task_list.html'

        return template_mapping.get(slug, default_template)

    def get(self, request,slug=None):
    
        user = request.user

        template_name = self.get_template_name(slug)
        tasks = Task.objects.filter(user=user)

        if slug == 'due-date':
            tasks = tasks.order_by('due_date')
        elif slug == 'priority':
            tasks = tasks.order_by('-priority')
        elif slug == 'category':
            tasks = tasks.order_by('category')
        else:
            tasks = Task.objects.filter(user=user)

        return render(request, template_name, {'tasks': tasks,'categories':categories})


class CompletedTaskListView(ListView):
    model = Task
    template_name = 'completed.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user,completed=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class RemainingTaskListView(ListView):
    model = Task
    template_name = 'remaining.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user,completed=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
        
class TaskCreateView(LoginRequiredMixin, FormView):
    template_name = 'add_task.html'
    success_url = '/'
    def get(self, request):
        form = TaskForm()
        categories = Category.objects.filter(user=request.user)
        return render(request, self.template_name, {'form': form,'categories':categories})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            task = form.save() 

            email_subject = 'Task Created Successfully'
            task_title=form.cleaned_data['title']
            email_body=render_to_string('task_created_confirmation.html',{'task':task,'user': task.user})
            email = EmailMultiAlternatives(email_subject,'',to=[task.user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return super().form_valid(form)
        return render(request, self.template_name, {'form': form})
    
class EditTaskView(LoginRequiredMixin,View):
    template_name='edit_task.html'

    def get(self,request,task_id):
        task = get_object_or_404(Task,id = task_id,user=request.user)
        user_categories = Category.objects.filter(user=request.user)
        form = TaskForm(instance=task,initial={'category': task.category})
        return render(request,self.template_name,{'form':form,'task':task_id,'user_categories': user_categories})
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.instance.user = self.request.user
            task = form.save() 
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'task_id': task_id})

class CategoryCreateView(View):
    template_name = 'category_form.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('add_task')
        return render(request, self.template_name, {'cat_form': form})

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class ToggleCompleteView(View):

    def get(self,request,task_id):
        task = get_object_or_404(Task, id=task_id)
        print(task)

        if task:
            task.completed = not task.completed
            task.save()
            if task.completed:

                email_subject = 'Task Completed'
                task_title=task.title
                email_body=render_to_string('task_completed_confirmation.html',{'task_title':task_title})
                email = EmailMultiAlternatives(email_subject,'',to=[task.user.email])
                email.attach_alternative(email_body,"text/html")
                email.send()
        return redirect('home')
    
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'delete.html', {
        "task": task,
    })

def remove_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task:
        task.delete()
        return redirect('home')   

