from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import (  TemplateView, 
                                    ListView, 
                                    DetailView, 
                                    UpdateView,
                                    CreateView
                                 )
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

from apps.userprofile.models import UserProfile
from apps.core_stuff.views import DebugMixin

from .models import Project
from .forms import ProjectForm
from .utils import ProjectPermissions

class ProjectIndexView(ProjectPermissions,ListView):
    model = Project
    template_name="projects/index.html"

class ProjectProposeView(LoginRequiredMixin, CreateView):
    model = Project
    template_name="projects/propose.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse("project_detail",args=(self.object.pk,))


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def post(self, request, *args, **kwargs):
        proj = self.get_object()
        if not request.user.is_authenticated():
       		#redirects to project detail page after signin, user needs to click apply button again
            #should user application be automatically be taken care of after successful login??? 
            url = "/accounts/login?next=" + reverse("project_detail",args=(proj.pk,proj.slug))
            return HttpResponseRedirect(url)
        else:
            if request.user.userprofile not in proj.applicants.all():
                proj.applicants.add(request.user.userprofile)
                #proj.save() #is this needed???
            
            return HttpResponseRedirect(reverse("project_detail",args=(proj.pk,proj.slug)))



class ProjectEditView(ProjectPermissions, UpdateView):
    model = Project
    template_name = "projects/edit.html"
    form_class = ProjectForm
    
    def get_success_url(self):
        return reverse("project_detail",args=(self.object.pk,))


###should this be a ListView instead with model = UserProfile???
class ProjectUsersView(DetailView):
    model = Project
    template_name = "projects/users.html"

    def get_queryset(self):
        queryset = super(ProjectUsersView,self).get_queryset()
        return queryset
    
    
### ???
class ProjectApplyView(DetailView):
    model = Project
    slug_field="name"
    slug_url_kwarg = "project"

class ProjectApplicantsView(ListView):
    model = UserProfile
