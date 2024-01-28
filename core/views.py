from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect
from tasks.models import Task,Category
from django.contrib import messages

# Create your views here.
def home(request,category_slug = None):
    user = request.user.id
    tasks = Task.objects.filter(user=user)

    if request.user.is_authenticated:
        all_categories  = Category.objects.filter(user=user).distinct()

        if category_slug is not None:
            category = get_object_or_404(Category,slug = category_slug,user=user)
            tasks = tasks.filter(category=category)
            categories = all_categories.exclude(id=category.id)

            if not tasks.exists():
                messages.warning(request, "No tasks found in this category.")
                return redirect('home')
        else:
            categories = all_categories 
        return render (request,'index.html',{'tasks':tasks,'categories':categories,'for_filter':'for_filter'})
    else:
        return render (request,'base.html')
    
def about_us(request):
        return render(request,'about_us.html')

def contact(request):
        return render(request,'contact.html')

def product(request):
    return render(request,'product.html')