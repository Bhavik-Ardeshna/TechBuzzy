from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from groups.models import Groups,GroupMember
from django.db import IntegrityError
from django.contrib import messages
from . import models

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = Groups
    fields = ['name','description']
    template_name = 'groups/group_form.html'

class GroupDetail(generic.DetailView):
    model = Groups
    template_name = 'groups/group_detail.html'

class GroupList(generic.ListView):
    model = Groups
    template_name = 'groups/group_list.html'

class JoinGroup(generic.RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(models.Groups,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user = self.request.user, group=group )
        except IntegrityError:
            messages.warning(self.request,"Warning, already a member of {}".format(group.name))
        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))
        return super().get(request,*args,**kwargs)

class LeaveGroup(generic.RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(group__slug=self.kwargs.get('slug')).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,"You can't leave this group because you aren't in it.")
        else:
            membership.delete()
            messages.success(self.request,"You have successfully left this group.")

        return super().get(request, *args, **kwargs)
