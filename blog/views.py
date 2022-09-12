from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView
from .models import Post


# Create your views here.

# def post_list(request):
#     posts = Post.published.all()
#     return render(request,'blog/list.html',{'posts':posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    return render(request,'blog/detail.html',{'post': post})

  
