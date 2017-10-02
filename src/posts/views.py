from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostCreateForm
# Create your views here.

# class PostTemplateView(TemplateView):
#     template_name = 'base.html'

# class PostListView(ListView):
#     def get_queryset(self):
#         slug = self.kwargs.get("slug")
#         if slug:
#             queryset = Post.objects.filter(
#                 Q(category__iexact= slug) | Q(category__icontains=slug)
#             )
#         else:
#             queryset = Post.objects.all()
#         return queryset

# class PostDetailView(DetailView):
#     queryset = Post.objects.all()
#     template_name = "post_detail.html"

#     def get_context_data(self, *args, **kwargs):
#         context = super(PostDetailView, self).get_context_data(*args,**kwargs)
#         return context


#     def get_object(self, *args, **kwargs):
#         post_id = self.kwargs.get('post_id')
#         obj = get_object_or_404(Post, id = post_id)
#         return obj

class PostListView(ListView):
    #queryset = Post.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q')
        # if query:
        #     print("Query is:", query)
        #     queryset = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        # else:
        #     queryset = Post.objects.all()
        queryset = Post.objects.search(query)
        return queryset

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PostListView, self).get_context_data(*args, **kwargs)
    #     print("Context is: ", context)
    #     print("Request is: ", self.request.GET.get('q'))

class PostDetailView(DetailView):

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if post_id:
            queryset = Post.objects.filter(pk = post_id)
        else:
            raise Http404
        return queryset

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        obj = get_object_or_404(self.get_queryset(), pk = post_id)
        return obj

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'posts/post_form.html'
    success_url   = '/posts/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "New Post"
        return context

