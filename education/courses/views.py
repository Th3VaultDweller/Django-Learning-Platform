from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Course

# Create your views here.


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseEditMixin, ListView):
    """CRUD for managing the course list"""

    model = Course
    template_name = "courses/manage/course/list.html"
    permission_required = "course.view_course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = "course.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = "course.change_course"


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "course.delete_course"
