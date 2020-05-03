from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.views import generic
from braces.views import SelectRelatedMixin
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . import models
from . import forms

User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')
    template_name = 'post/post_list.html'

class UserPostList(generic.ListView):
    model = models.Post
    template_name = 'post/user_post_list.html'

    # Now get the queryset of post of current user and take from all posts
    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetailView(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')
    template_name = 'post/post_detail.html'

    # Collecting all post of current user from all post
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class PostCreateView(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    model = models.Post
    fields = ('group','message')
    template_name = 'post/post_form.html'

    def form_valid(self, form):
        # request.user typically returns an instance of django.contrib.auth.models.User, although the behavior depends on the authentication policy being used.
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')
    template_name = 'post/post_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args, **kwargs):
        messages.success(self.request,'Post deleted successfully !')
        return super().delete(*args, **kwargs)

