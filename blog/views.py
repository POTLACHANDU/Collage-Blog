from django.shortcuts import render
from django.views.generic import ListView
from . models import post



def home(request):
    #posts = post.objects.order_by('date_posted')

    context = {
        'posts':post.objects.all()
    }
    #return render(request, 'blog/home.html', {'posts': posts})
    post.objects.order_by('creation_time')
    return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    #ordering = ['-date_posted']

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
