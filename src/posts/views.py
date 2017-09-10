from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from .models import Post
from django.db.models import Q
# Create your views here.

class PostTemplateView(TemplateView):
    template_name = 'base.html'

class PostListView(ListView):
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Post.objects.filter(
                Q(category__iexact= slug) | Q(category__icontains=slug)
            )
        else:
            queryset = Post.objects.all()
        return queryset

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = "post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        return context


    def get_object(self, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        obj = get_object_or_404(Post, id = post_id)
        return obj