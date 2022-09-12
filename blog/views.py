from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail


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

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                        post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',
                        [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,
                                                'form': form,
                                                'sent': sent})

# def post_share(request,post_id):
#     #retrieve post by id
#     # post = get_object_or_404(Post, id=post_id, status='published')
#     post = get_object_or_404(Post, id=post_id, status='published')
#     sent = False

#     if request.method == 'POST':
#         #form was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             #Form fields passed validation
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(
#                         post.get_absolute_url())
#             subject = f"{cd['name']} recommends you read " \
#                 f"{post.title}"
#             message = f"Read {post.title} at {post_url}\n\n" \
#                     f"{cd['name']}\'s comments: {cd['comments']}"
#             send_mail(subject, message, 'admin@myblog.com',
#                         [cd['to']])
#             sent = True

#             #...send email
#         else:
#             form = EmailPostForm()
#             context = {'post':post,'form':form,'sent':sent}
#         return render(request,'blog/share.html',context)

  
