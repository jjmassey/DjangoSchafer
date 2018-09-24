from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import JobListing


class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobListing
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class JobPageView(ListView):
	model = JobListing
	template_name = 'jobs/jobs.html'
	context_object_name = 'data'
	ordering = ['-date_posted']

class UserJobPageView(ListView):
	model = JobListing
	template_name = 'user_jobs.html'
	context_object_name = 'data'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return JobListing.objects.filter(author=user).order_by('-date_posted')

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobListing
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobListing
    success_url = '/'   # redirect to home page once deleted

    def test_func(self):
        job = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class JobDetailView(DetailView):
    model = JobListing
